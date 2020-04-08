from django.core.management.base import BaseCommand

from proxy.models import Document, Domain


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--domain', '-d', nargs='?', type=str, default=None)

    def handle(self, *args, **options):
        domain_arg = options.get('domain', None)

        if domain_arg:
            domain = Domain.objects.get(domain=domain_arg)
            docs = Document.objects.filter(domain=domain)

            cont = input(f'Are you sure you want to delete all of {domain}? ({docs.count()} documents) (y/n)? ')
            if cont == 'y' or cont == 'yes':
                domain.delete()
                docs.delete()

        else:
            docs = Document.objects.all()
            domains = Domain.objects.all()

            cont = input(f'Are you sure you want to delete {docs.count()} documents and {domains.count()} domains (y/n)? ')
            if cont == 'y' or cont == 'yes':
                docs.delete()
                domains.delete()

