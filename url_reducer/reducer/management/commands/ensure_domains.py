import os
import re

from django.core.management.base import BaseCommand
from reducer.models import Domain

BASE_DIR = os.getcwd()
DOMAINS_FILE = os.path.join(BASE_DIR, 'domains')


class Command(BaseCommand):
    help = "Creates available domains"

    def handle(self, *args, **options):
        with open(DOMAINS_FILE, 'r') as df:
            for domain_name in df:
                dn = re.sub('\n', '', domain_name)
                Domain.objects.get_or_create(domain=dn)





