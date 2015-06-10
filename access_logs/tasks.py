import re
import dateutil.parser
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings

from .models import AccessLog

regex = re.compile(r"(?P<remote_host>\S*)\s-\s(?P<remote_user>\S*)\s\[(?P<timestamp>.*?)\]\s{1,2}\"(?P<http_method>\S*)\s*(?P<request>\S*)\s*(HTTP\/)*(?P<http_version>.*?)\"\s(?P<status>\d{3})\s(?P<bytes_sent>\S*)\s\"(?P<referer>[^\"]*)\"\s\"(?P<user_agent>[^\"]*)\"\s(?P<request_time>\S*)\s(?P<upstream_response_time>\S*)\s(?P<pipe>\S*)")

# Run before logrorate rotates the file
@periodic_task(run_every=crontab(minute=23, hour=6))
def parse_access_log():
    parse_access_log_file(settings.ACCESS_LOG_PATH)


def parse_access_log_file(file_path):
    errors = {}
    with open(file_path, 'r') as log_file:
        for line in log_file:
            try:
                r = regex.search(line.strip())
                if r is None:
                    continue
                data = r.groupdict()
                if re.search("(\.gif|\.jpg|\.png|\.css|\.js|\.ico|\.txt)/?$", data['request']):
                    continue
                if any(map(lambda x: len(data.get(x)) > 500, ['http_method', 'http_version', 'user_agent'])):
                    continue
                data['timestamp'] = dateutil.parser.parse(data['timestamp'], fuzzy=True)
                AccessLog.objects.get_or_create(**data)
            # pylint: disable=W0703
            except Exception as e:
                errors[line] = e

    if errors:
        raise Exception(errors)