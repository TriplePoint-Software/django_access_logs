# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_logs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLogConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_agent_bot_list', models.TextField(default=b'cloudflare, twiceler, yahooseeker, chtml, generic, heritrix, attentio, fast, mediapartners, python, experiment, fastmobilecrawl, curl, yahooysmcm, crawl, bingbot, bot, borg, google(^tv), yahoo, slurp, msnbot, msrbot, openbot, archiver, netresearch, lycos, scooter, altavista, teoma, gigabot, baiduspider, blitzbot, oegp, charlotte, furlbot, http%20client, polybot, htdig, ichiro, mogimogi, larbin, pompos, scrubby, searchsight, seekbot, semanticdiscovery, silk, snappy, speedy, spider, voila, vortex, voyager, zao, zeal, fast\\-webcrawler, converacrawler, dataparksearch, findlinks, crawler, Netvibes, Sogou Pic Spider, ICC\\-Crawler, Innovazion Crawler, Daumoa, EtaoSpider, A6\\-Indexer, YisouSpider, Riddler, DBot, wsr\\-agent, Xenu, SeznamBot, PaperLiBot, SputnikBot, CCBot, ProoXiBot, Scrapy, Genieo, Screaming Frog, YahooCacheSystem, CiBra, Nutch, holmes, WebThumbnail, ^voyager, heritrix, scraper, favicon, Google.*/\\+/web/snippet, Icarus6j, PagePeeker, ^vortex, Sogou, ^Java/, BlogBridge, ZooShot, indexer, GomezAgent, ^JNLP/, ^NING, WinHTTP, TLSProber, Squrl Java, NewsGator, Google-HTTP-Java-Client, Reaper, WhatWeb, crawl, facebookexternalhit, Python-urllib, IlTrovatore-Setaccio, AppEngine-Google, InternetArchive, WordPress, Retreiver')),
                ('access_log_export_excluded_ips', models.TextField(default=b'')),
            ],
            options={
                'verbose_name': 'Access Log Configuration',
            },
        ),
    ]
