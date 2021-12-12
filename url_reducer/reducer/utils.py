import random
import time
from datetime import timedelta

import redis
from django.conf import settings

from reducer.models import URLs
from reducer.serializers import SAMPLE_URL_SYMBOLS


def get_urls_cache_generator():
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=0,
                                       socket_connect_timeout=1)
    is_connect = False
    max_connect_attempts = 3

    while True:

        if not settings.DEBUG:
            try:
                is_connect = redis_instance.ping()

            except (ConnectionError, TimeoutError,
                    redis.exceptions.ConnectionError,
                    redis.exceptions.TimeoutError):
                is_connect = False

        if is_connect:

            url, url_destination = yield

            if url and url_destination:
                redis_instance.setex(url, timedelta(minutes=20), url_destination)
                yield True

            elif url and not url_destination:
                try:
                    cached_url = redis_instance.get(url).decode('utf-8')
                    yield cached_url

                except AttributeError:
                    cached_url = URLs.objects.get(url=url)
                    redis_instance.setex(url, timedelta(minutes=40000), cached_url.url_destination)

                    yield cached_url.url_destination

            else:
                pass

        else:
            time.sleep(2)
            max_connect_attempts -= 1

            if max_connect_attempts == 0:
                break


def short_url_generator(url=None):
    if url:
        """ Set manually url subpart """
        check_exist_subpart = URLs.objects.filter(url=url)

        if check_exist_subpart.exists():
            return False

        return url

    else:

        min_url_length = 5
        attempts = 0

        random.shuffle(SAMPLE_URL_SYMBOLS)

        while True:
            """ Generate randomized URL subpart """
            try:
                attempts += 1

                if attempts > 5:
                    min_url_length += 1
                    attempts = 0

                sample = SAMPLE_URL_SYMBOLS[0:min_url_length]
                reduced_url = ''.join(random.sample(sample, min_url_length))
                check_short_url = URLs.objects.filter(url=reduced_url)

                if check_short_url.exists():
                    min_url_length += 1
                else:
                    return reduced_url

            except ValueError:
                min_url_length += 1
