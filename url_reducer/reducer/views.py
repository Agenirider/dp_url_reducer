import random
import string
import time
from datetime import timedelta

import redis
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import TemplateDoesNotExist
from reducer.models import URLs, Domain
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from utils.user_uuid_handler import user_uuid_handler


def get_urls_cache_generator():
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=0,
                                       socket_connect_timeout=1)
    is_connect = False
    max_connect_attempts = 5

    while True:

        if not settings.DEBUG:
            try:
                is_connect = redis_instance.ping()

            except (ConnectionError, TimeoutError, redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
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
                break

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
        """ Generate randomized URL subpart """
        sample = string.ascii_lowercase + string.ascii_uppercase + string.digits
        reduced_url = ''.join(random.sample(list(sample), 7))

        try:
            """ Check is exist generated URL """
            check_short_url = URLs.objects.get(url=reduced_url)
            if check_short_url:
                short_url_generator(None)

        except URLs.DoesNotExist:
            return reduced_url

        return False


cashed_urls = get_urls_cache_generator()
try:
    cashed_urls.send(None)
except StopIteration:
    cashed_urls = None


class URLsSerializer(serializers.Serializer):
    url_destination = serializers.CharField(max_length=500)
    domain = serializers.IntegerField(max_value=9999)
    url = serializers.CharField(default=None, max_length=200, allow_blank=True)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def set_url(request):
    user = user_uuid_handler(request)

    serializer = URLsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    err = serializer.errors

    if err:
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.data

    response = Response()
    response.set_cookie('dp_test_user_id', user.user_uuid, max_age=999999999)

    if serializer.is_valid():

        generated_url = short_url_generator(data.get('url'))

        url_destination = data.get('url_destination')

        try:
            domain = Domain.objects.get(pk=data.get('domain'))
        except Domain.DoesNotExist:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response

        if generated_url:
            new_url = URLs(user_uuid=user,
                           url=generated_url,
                           domain=domain,
                           url_destination=url_destination)
            new_url.save()

            if cashed_urls:
                cashed_urls.send((generated_url, url_destination))
                cashed_urls.send(())

            response.status_code = status.HTTP_200_OK
            response.data = {'res': 'url_created',
                             'url': f'{domain.domain}/{generated_url}'}

            return response

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            response.data = {'res': 'url_already_exists'}

            return response


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_url(request, page_num):
    user = user_uuid_handler(request)
    urls = list(URLs.objects.select_related('domain').filter(user_uuid=user)[page_num * 10:(page_num + 1) * 10])

    extracted_urls = [{'id': url.id,
                       'domain': url.domain.domain,
                       'url': url.url,
                       'url_destination': url.url_destination} for url in urls]

    response = Response({'res': extracted_urls,
                         'prev_page': False if page_num == 0 else True,
                         'next_page': False if len(urls) < 10 else True},
                        status=status.HTTP_200_OK)

    response.set_cookie('dp_test_user_id', user.user_uuid, max_age=999999999)
    return response


@api_view(['DELETE'])
@permission_classes([AllowAny, ])
def delete_url(request, url_id):
    user = user_uuid_handler(request)
    URLs.objects.filter(pk=url_id, user_uuid=user).delete()
    response = Response(status=status.HTTP_200_OK)
    response.set_cookie('dp_test_user_id', user.user_uuid, max_age=999999999)
    return response


@api_view(['GET'])
@permission_classes([AllowAny, ])
def redirect_url(request, domain, domain_subpart):
    try:
        domain = Domain.objects.get(domain=domain)
        url_destination = URLs.objects.get(domain=domain, url=domain_subpart)
        url = url_destination.url_destination

        return redirect(url,  permanent=False)

    except (URLs.DoesNotExist, TemplateDoesNotExist):
        return Response({'reason': 'URL NOT FOUND',
                         'source': f'{domain}|{domain_subpart}'},
                        status=status.HTTP_404_NOT_FOUND)

