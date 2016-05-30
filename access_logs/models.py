from django.db import models
from ua_parser import user_agent_parser
from solo.models import SingletonModel


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
        ordering = ('-timestamp',)

    def user_agent_display(self):
        info = user_agent_parser.Parse(self.user_agent)
        return "%s %s %s" % (info['os']['family'] or '',
                             info['user_agent']['family'] or '',
                             info['user_agent']['major'] or '')

    user_agent_display.short_description = 'User agent'


BOT_LIST = ['cloudflare', 'twiceler', 'yahooseeker', 'chtml', 'generic', 'heritrix', 'attentio', 'fast',
            'mediapartners', 'python', 'experiment', 'fastmobilecrawl', 'curl',
            'yahooysmcm', 'crawl', 'bingbot', 'bot', 'borg', 'google(^tv)', 'yahoo', 'slurp', 'msnbot', 'msrbot',
            'openbot', 'archiver', 'netresearch', 'lycos', 'scooter',
            'altavista', 'teoma', 'gigabot', 'baiduspider', 'blitzbot', 'oegp', 'charlotte', 'furlbot', 'http%20client',
            'polybot', 'htdig', 'ichiro', 'mogimogi', 'larbin',
            'pompos', 'scrubby', 'searchsight', 'seekbot', 'semanticdiscovery', 'silk', 'snappy', 'speedy', 'spider',
            'voila', 'vortex', 'voyager', 'zao', 'zeal',
            'fast\-webcrawler', 'converacrawler', 'dataparksearch', 'findlinks', 'crawler', 'Netvibes',
            'Sogou Pic Spider', 'ICC\-Crawler', 'Innovazion Crawler', 'Daumoa',
            'EtaoSpider', 'A6\-Indexer', 'YisouSpider', 'Riddler', 'DBot', 'wsr\-agent', 'Xenu', 'SeznamBot',
            'PaperLiBot', 'SputnikBot', 'CCBot', 'ProoXiBot', 'Scrapy',
            'Genieo', 'Screaming Frog', 'YahooCacheSystem', 'CiBra', 'Nutch', 'holmes', 'WebThumbnail', '^voyager',
            'heritrix', 'scraper', 'favicon', 'Google.*/\\+/web/snippet',
            'Icarus6j', 'PagePeeker', '^vortex', 'Sogou', '^Java/', 'BlogBridge', 'ZooShot', 'indexer', 'GomezAgent',
            '^JNLP/', '^NING', 'WinHTTP', 'TLSProber', 'Squrl Java',
            'NewsGator', 'Google-HTTP-Java-Client', 'Reaper', 'WhatWeb', 'crawl', 'facebookexternalhit',
            'Python-urllib', 'IlTrovatore-Setaccio', 'AppEngine-Google',
            'InternetArchive', 'WordPress', 'Retreiver']


class AccessLogConfiguration(SingletonModel):
    user_agent_bot_list = models.TextField(default=', '.join(BOT_LIST))
    access_log_export_excluded_ips = models.TextField(default='')

    def __unicode__(self):
        return u"Access Log Configuration"

    class Meta:
        verbose_name = "Access Log Configuration"
