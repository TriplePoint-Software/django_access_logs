import datetime

import import_export
import pytz
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from import_export import admin as import_export_admin
from import_export import fields, resources
from import_export import forms as import_export_forms
from solo.admin import SingletonModelAdmin

from .models import AccessLog, AccessLogConfiguration


def make_tz_aware(dt, tz='UTC', is_dst=None):
    """Add timezone information to a datetime object, only if it is naive."""
    tz = dt.tzinfo or tz
    try:
        tz = pytz.timezone(tz)
    except AttributeError:
        pass
    return tz.localize(dt, is_dst=is_dst)

class AccessLogResource(resources.ModelResource):
    user_agent_raw = fields.Field()

    class Meta:
        model = AccessLog
        export_order = ('id', 'timestamp', 'bytes_sent', 'referer', 'request', 'http_method', 'http_version',
                        'remote_host', 'remote_login', 'remote_user', 'status', 'user_agent', 'user_agent_raw',
                        'request_time', 'upstream_response_time', 'pipe')

    def dehydrate_timestamp(self, access_log):
        return make_tz_aware(access_log.timestamp, settings.TIME_ZONE).strftime("%m/%d/%y %H:%M:%S")

    def dehydrate_user_agent(self, access_log):
        return access_log.user_agent_display()

    def dehydrate_user_agent_raw(self, access_log):
        return access_log.user_agent


class CustomExportForm(import_export_forms.ExportForm):
    file_format = forms.ChoiceField(label='Format*', choices=())
    start_date = forms.DateField(label='Start Date', required=False, widget=admin.widgets.AdminDateWidget())
    end_date = forms.DateField(label='End Date', required=False, widget=admin.widgets.AdminDateWidget())
    status = forms.ChoiceField(label='Status', required=False, choices=())
    filter_bots = forms.BooleanField(label="Filter Bots", required=False, initial=True)
    filter_admin_ips = forms.ChoiceField(label="Filter Admin IPs?", required=False, initial=90,
                                         choices=((90, 'From last 90 days'), (60, 'From the last 60 days'),
                                                  (30, 'From last 30 days'), ('', 'Don\'t Filter')))

    def __init__(self, formats, *args, **kwargs):
        super(CustomExportForm, self).__init__(formats, *args, **kwargs)
        status_list = AccessLog.objects.order_by().values_list('status', flat=True).distinct()
        self.fields['status'].choices = [('', 'All')] + [(e, e) for e in status_list]

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be lesser than Start date")
        return self.cleaned_data['end_date']


class CustomExportMixin(import_export_admin.ExportMixin):
    export_template_name = 'admin/import_export/export.html'

    def get_export_formats(self):
        return [import_export.formats.base_formats.CSV, ]

    def get_export_queryset(self, request, cleaned_data=None):
        # can't manipulate/replace the queryset filters once added
        # http://stackoverflow.com/questions/5220433/how-to-edit-filters-list-of-a-queryset
        # http://stackoverflow.com/questions/4689566/django-remove-a-filter-condition-from-a-queryset
        # need to manipulate the request.GET multidict
        GET = request.GET.copy()
        export_params = [('start_date', 'timestamp__gte'), ('end_date', 'timestamp__lt'), ('status', 'status')]
        for field_name, param in export_params:
            if cleaned_data.get(field_name) is not None and GET.get(param):
                GET.pop(param)
        request = HttpRequest()
        request.GET = GET
        queryset = super(CustomExportMixin, self).get_export_queryset(request)

        if cleaned_data.get('start_date'):
            queryset = queryset.filter(timestamp__gte=cleaned_data['start_date'])

        if cleaned_data.get('end_date'):
            end_timestamp = datetime.datetime.combine(cleaned_data['end_date'], datetime.time.max)
            queryset = queryset.filter(timestamp__lte=end_timestamp)

        if cleaned_data.get('status'):
            queryset = queryset.filter(status=cleaned_data['status'])

        config = AccessLogConfiguration.objects.get()
        if cleaned_data.get('filter_bots'):
            config_agents = config.user_agent_bot_list.strip().split(',')
            user_agent_iregex = '(' + '|'.join([uas.strip() for uas in config_agents]) + ')'
            queryset = queryset.exclude(Q(user_agent__iregex=r'(%s)' % user_agent_iregex) | Q(user_agent='-'))

        if cleaned_data.get('filter_admin_ips'):
            start_date = datetime.datetime.today() - datetime.timedelta(days=int(cleaned_data['filter_admin_ips']))

            admin_ips = set(AccessLog.objects.filter(timestamp__gt=start_date, request__istartswith='/admin')
                            .values_list('remote_host', flat=True))
            config_excluded_ips = config.access_log_export_excluded_ips.strip().split(',')
            excluded_ips = [ip.strip() for ip in config_excluded_ips] + list(admin_ips)
            queryset = queryset.exclude(remote_host__in=excluded_ips)
        return queryset

    def export_action(self, request, *args, **kwargs):
        formats = self.get_export_formats()

        start_date = None
        if request.GET.get('timestamp__gte'):
            start_date = datetime.datetime.strptime(request.GET['timestamp__gte'].split(' ')[0], '%Y-%m-%d')

        end_data = None
        if request.GET.get('timestamp__lt'):
            end_data = datetime.datetime.strptime(request.GET['timestamp__lt'].split(' ')[0], '%Y-%m-%d')

        status = request.GET.get('status', None) or None

        initial_data = {
            'start_date': start_date,
            'end_date': end_data,
            'status': status
        }

        form = CustomExportForm(formats, request.POST or None, initial=initial_data)
        if form.is_valid():
            file_format = formats[int(form.cleaned_data['file_format'])]()

            queryset = self.get_export_queryset(request, cleaned_data=form.cleaned_data)
            export_data = self.get_export_data(file_format, queryset)
            content_type = 'application/octet-stream'
            # Django 1.7 uses the content_type kwarg instead of mimetype
            try:
                response = HttpResponse(export_data, content_type=content_type)
            except TypeError:
                response = HttpResponse(export_data, mimetype=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                self.get_export_filename(file_format),
            )
            return response

        context = {
            'form': form,
            'opts': self.model._meta,
        }

        if request.GET.get('q'):
            context['search_term'] = request.GET.get('q')

        return TemplateResponse(request, [self.export_template_name], context, current_app=self.admin_site.name)


class HTTPMethodListFilter(SimpleListFilter):
    title = "Http Method"
    parameter_name = "http_method"

    def lookups(self, request, model_admin):
        return [('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('HEAD', 'HEAD'),
                ('OPTIONS', 'OPTIONS'), ('DELETE', 'DELETE')]

    def queryset(self, request, qs):
        if self.value():
            qs = qs.filter(http_method__iexact=self.value())
        return qs


class AccessLogAdmin(CustomExportMixin, admin.ModelAdmin):
    list_display = ['timestamp', 'remote_host', 'status',
                    'http_method', 'request', 'referer',
                    'bytes_sent', 'http_version', 'user_agent_display',
                    'request_time', 'upstream_response_time', 'pipe']
    list_filter = ['timestamp', 'status', HTTPMethodListFilter]
    search_fields = ['timestamp', 'bytes_sent', 'referer',
                     'request', 'remote_host', 'status',
                     'user_agent']

    list_display_links = None
    resource_class = AccessLogResource

    class Media:
        js = ('js/list_filter_collapse.js',)

    def has_change_permission(self, request, obj=None):
        return obj is None

    def has_add_permission(self, request):
        return False

    def has_save_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False


admin.site.register(AccessLog, AccessLogAdmin)


admin.site.register(AccessLogConfiguration, SingletonModelAdmin)


