from django.shortcuts import redirect
from reducer.models import URLs, Domain
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.user_uuid_handler import user_uuid_handler
from reducer.serializers import URLsSerializer, URLsDBSerializer
from reducer.utils import get_urls_cache_generator, short_url_generator
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

""" Init cache access """
cashed_urls = get_urls_cache_generator()
try:
    cashed_urls.send(None)
except StopIteration:
    cashed_urls = None


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

        generated_url = short_url_generator(url=data.get('url'))

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

            logger.info(f'Add new url -> {domain.domain}/{generated_url}')

            return response

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            response.data = {'res': 'url_already_exists'}

            return response


class NotFoundError:
    pass


class CustomPaginator(PageNumberPagination):
    page_size = 10

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({"error": "No results found for the requested page"},
                            status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)


class UrlList(APIView):
    def get(self, request, page_num, format=None):
        user = user_uuid_handler(request)

        urls = list(URLs.objects.select_related('domain').filter(user_uuid=user))
        paginator = CustomPaginator()
        response = paginator.generate_response(urls, URLsDBSerializer, request)
        return response


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_domains(request):
    domains = list(Domain.objects.all())
    res = []
    for domain in domains:
        res.append({'id': domain.id, 'domain': domain.domain})

    return Response(res, status=status.HTTP_200_OK)


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
        if cashed_urls:
            url = cashed_urls.send((domain_subpart, None))

        else:
            domain = Domain.objects.get(domain=domain)
            url_destination = URLs.objects.get(domain=domain, url=domain_subpart)
            url = url_destination.url_destination

        return redirect(f'https://{url}')

    except URLs.DoesNotExist:
        logger.error('Unknown URL')
        return Response({'reason': 'URL NOT FOUND',
                         'source': f'{domain}/{domain_subpart}'},
                        status=status.HTTP_404_NOT_FOUND)
