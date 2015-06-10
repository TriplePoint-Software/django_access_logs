
from django.db import models
from ua_parser import user_agent_parser


class AccessLog(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    bytes_sent = models.CharField(max_length=500)
    referer = models.TextField()
    request = models.TextField()
    http_method = models.CharField(max_length=500)
    http_version = models.CharField(max_length=500)
    remote_host = models.CharField(max_length=500)
    remote_login = models.CharField(max_length=500)
    remote_user = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    user_agent = models.CharField(max_length=500)
    request_time = models.CharField(max_length=500)
    upstream_response_time = models.CharField(max_length=500)
    pipe = models.CharField(max_length=500)

    class Meta:
        ordering = ('-timestamp', )

    def user_agent_display(self):
        info = user_agent_parser.Parse(self.user_agent)
        return "%s %s %s" % (info['os']['family'] or '',
                             info['user_agent']['family'] or '',
                             info['user_agent']['major'] or '')
    user_agent_display.short_description = 'User agent'
