from django.core.management.base import BaseCommand

from reducer.models import Domain

domains = ['domain1.link',
           'dom123.com',
           'test123.ru',
           'lalala.we',
           'blablabla.com',
           ]


class Command(BaseCommand):
    help = "Creates available domains"

    def handle(self, *args, **options):

        for domain in domains:
            Domain.objects.get_or_create(domain=domain)





