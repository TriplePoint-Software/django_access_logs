import datetime
import pytz

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse

from constance import config
import import_export
from import_export import admin as import_export_admin
from import_export import forms as import_export_forms
from import_export import fields, resources

from .models import AccessLog


class AccessLogResource(resources.ModelResource):
    user_agent_raw = fields.Field()

    class Meta:
        model = AccessLog
        export_order = ('id', 'timestamp', 'bytes_sent', 'referer', 'request', 'http_method', 'http_version',
                        'remote_host', 'remote_login', 'remote_user', 'status', 'user_agent', 'user_agent_raw',
                        'request_time', 'upstream_response_time', 'pipe')

    def dehydrate_timestamp(self, access_log):
        return access_log.timestamp.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%m/%d/%y %H:%M:%S")

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
        self.fields['status'].choices = [('', 'All')] + \
                                        [(e, e) for e in
                                         AccessLog.objects.order_by().values_list('status', flat=True).distinct()]

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
        get_params = request.GET.copy()
        for field_name, param in [('start_date', 'timestamp__gte'), ('end_date', 'timestamp__lt'),
                                  ('status', 'status')]:
            if cleaned_data.get(field_name) is not None and get_params.get(param):
                get_params.pop(param)
        req = HttpRequest()
        req.GET = get_params
        queryset = super(CustomExportMixin, self).get_export_queryset(req)
        if cleaned_data.get('start_date'):
            queryset = queryset.filter(timestamp__gte=cleaned_data['start_date'])
        if cleaned_data.get('end_date'):
            end_timestamp = datetime.datetime.combine(cleaned_data['end_date'], datetime.time.max)
            queryset = queryset.filter(timestamp__lte=end_timestamp)
        if cleaned_data.get('status'):
            queryset = queryset.filter(status=cleaned_data['status'])
        if cleaned_data.get('filter_bots'):
            user_agent_iregex = '(' + '|'.join([uas.strip() for uas in config.USER_AGENT_BOT_LIST.strip().split(',')]) \
                                + ')'
            queryset = queryset.exclude(Q(user_agent__iregex=r'(%s)' % user_agent_iregex) | Q(user_agent='-'))
        if cleaned_data.get('filter_admin_ips'):
            start_date = datetime.datetime.today() - datetime.timedelta(days=int(cleaned_data['filter_admin_ips']))
            admin_ips = set(AccessLog.objects.filter(timestamp__gt=start_date, request__istartswith='/admin')
                            .values_list('remote_host', flat=True))
            excluded_ips = [ip.strip() for ip in config.ACCESS_LOG_EXPORT_EXCLUDED_IPS.strip().split(',')] \
                           + list(admin_ips)
            queryset = queryset.exclude(remote_host__in=excluded_ips)
        return queryset

    def export_action(self, request, *args, **kwargs):
        formats = self.get_export_formats()
        initial_data = {
            'start_date': datetime.datetime.strptime(request.GET['timestamp__gte'].split(' ')[0], '%Y-%m-%d')
            if request.GET.get('timestamp__gte') else None,
            'end_date': datetime.datetime.strptime(request.GET['timestamp__lt'].split(' ')[0], '%Y-%m-%d')
            if request.GET.get('timestamp__lt') else None,
            'status': request.GET['status'] if request.GET.get('status') else None
        }

        form = CustomExportForm(formats, request.POST or None, initial=initial_data)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()

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

        context = {}
        context['form'] = form
        if request.GET.get('q'):
            context['search_term'] = request.GET.get('q')
        context['opts'] = self.model._meta
        return TemplateResponse(request, [self.export_template_name],
                                context, current_app=self.admin_site.name)


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
    resource_class = AccessLogResource

    class Media:
        js = ('js/list_filter_collapse.js',)


admin.site.register(AccessLog, AccessLogAdmin)
