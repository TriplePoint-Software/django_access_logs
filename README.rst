**A simple reusable Django app to record parsed server access logs in a database and export them as CSV on demand**

**Pre-requisites** (*should be taken care of by setup.py automatically*)

    ``django-constance >= 0.6``

    ``ua-parser >= 0.3.6``

    ``django-import-export >= 0.2.7``

    ``python-dateutil >= 2.4.2``

    ``celery >= 3.1.18``

    ``django-celery >= 3.1.16``
    
*If you are using Django < 1.7. Use the Django_lt_1.7 branch and install* ``south``    

**Settings Required**

    ::

      CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

      BOT_LIST = ['cloudflare', 'twiceler', 'yahooseeker', 'chtml', 'generic', 'heritrix', 'attentio', 'fast', 'mediapartners', 'python', 'experiment', 'fastmobilecrawl', 'curl',
            'yahooysmcm', 'crawl', 'bingbot', 'bot', 'borg', 'google(^tv)', 'yahoo', 'slurp', 'msnbot', 'msrbot', 'openbot', 'archiver', 'netresearch', 'lycos', 'scooter',
            'altavista', 'teoma', 'gigabot', 'baiduspider', 'blitzbot', 'oegp', 'charlotte', 'furlbot', 'http%20client', 'polybot', 'htdig', 'ichiro', 'mogimogi', 'larbin',
            'pompos', 'scrubby', 'searchsight', 'seekbot', 'semanticdiscovery', 'silk', 'snappy', 'speedy', 'spider', 'voila', 'vortex', 'voyager', 'zao', 'zeal',
            'fast\-webcrawler', 'converacrawler', 'dataparksearch', 'findlinks', 'crawler', 'Netvibes', 'Sogou Pic Spider', 'ICC\-Crawler', 'Innovazion Crawler', 'Daumoa',
            'EtaoSpider', 'A6\-Indexer', 'YisouSpider', 'Riddler', 'DBot', 'wsr\-agent', 'Xenu', 'SeznamBot', 'PaperLiBot', 'SputnikBot', 'CCBot', 'ProoXiBot', 'Scrapy',
            'Genieo', 'Screaming Frog', 'YahooCacheSystem', 'CiBra', 'Nutch', 'holmes', 'WebThumbnail', '^voyager', 'heritrix', 'scraper', 'favicon', 'Google.*/\\+/web/snippet',
            'Icarus6j', 'PagePeeker', '^vortex', 'Sogou', '^Java/', 'BlogBridge', 'ZooShot', 'indexer', 'GomezAgent', '^JNLP/', '^NING', 'WinHTTP', 'TLSProber', 'Squrl Java',
            'NewsGator', 'Google-HTTP-Java-Client', 'Reaper', 'WhatWeb', 'crawl', 'facebookexternalhit', 'Python-urllib', 'IlTrovatore-Setaccio', 'AppEngine-Google',
            'InternetArchive', 'WordPress', 'Retreiver']
 
      CONSTANCE_CONFIG = {
        'USER_AGENT_BOT_LIST': (', '.join(BOT_LIST), 'Comma separated bot names used in user agent bot detection regex'),
        'ACCESS_LOG_EXPORT_EXCLUDED_IPS': ('', 'Comma separated IP addresses to be excluded from Access Log Export')
      }


