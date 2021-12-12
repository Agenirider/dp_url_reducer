import string

from rest_framework import serializers

SAMPLE_URL_SYMBOLS = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_-')


def check_allowed_url_symbols(url):
    split_url = list(url)

    for s in split_url:
        if s not in SAMPLE_URL_SYMBOLS:
            raise serializers.ValidationError('Unallowed symbols in URL.')


class URLsSerializer(serializers.Serializer):
    url_destination = serializers.CharField(max_length=500)
    domain = serializers.IntegerField(max_value=9999)
    url = serializers.CharField(default=None,
                                max_length=200,
                                allow_blank=True,
                                validators=[check_allowed_url_symbols])


class URLsDBSerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=300)
    id = serializers.IntegerField(max_value=9999)
    url = serializers.CharField(max_length=300)
    url_destination = serializers.CharField(max_length=300)