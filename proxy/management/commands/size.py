from django.core.management.base import BaseCommand

from proxy.models import Document, Domain


class Command(BaseCommand):
    def handle(self, *args, **options):

        def format_size(nb):
            if nb < 1e3:
                return f'{nb}B'
            elif nb < 1e6:
                return f'{int(nb / 100) / 10}KB'
            elif nb < 1e9:
                return f'{int(nb / 100000) / 10}MB'
            elif nb < 1e12:
                return f'{int(nb / 100000000) / 10}GB'

        def show_table(parts):
            n = len(parts[0])
            ms = [0 for i in range(n)]
            for p in parts:
                for i in range(n):
                    if len(p[i]) > ms[i]:
                        ms[i] = len(p[i])

            for p in parts:
                line = ''
                for i in range(n):
                    line += p[i] + (' ' * (ms[i] - len(p[i]))) + '  '
                print(line)

        domains = Domain.objects.all()
        total_size = 0
        total_mime = {}
        total_mime_s = {}

        # print('')
        parts = [('', '', '')]
        for domain in domains:
            docs = Document.objects.filter(domain=domain)

            domain_size = 0
            mimes = {}
            mimes_s = {}
            for doc in docs:
                ds = len(doc.content)
                key = doc.mime.split(';')[0]

                if key not in mimes:
                    mimes[key] = 1
                    mimes_s[key] = 0
                else:
                    mimes[key] += 1
                    mimes_s[key] += ds

                if key not in total_mime:
                    total_mime[key] = 1
                    total_mime_s[key] = 0
                else:
                    total_mime[key] += 1
                    total_mime_s[key] += ds

                domain_size += ds
                total_size += ds

            # print(f'{domain}: {format_size(domain_size)}')
            parts += [
                ('', '', ''),
                (f'{domain}:', format_size(domain_size), str(docs.count())),
                ('Mime', 'size', 'N'),
            ]

            np = []
            for key in mimes:
                np += [(f'{key}', f'{format_size(mimes_s[key])}', f'{mimes[key]}')]
            np = list(reversed(sorted(np, key=lambda p: 1e999 if p[2] == 'N' else int(p[2]))))
            parts += np + [('', '', '')]
            # print('')

        parts += [
            ('', '', ''),
            (f'Everything', format_size(total_size), str(Document.objects.all().count())),
            ('Mime', 'size', 'N'),
        ]

        np = []
        for key in total_mime:
            np += [(f'{key}', f'{format_size(total_mime_s[key])}', f'{total_mime[key]}')]
        np = list(reversed(sorted(np, key=lambda p: 1e999 if p[2] == 'N' else int(p[2]))))
        parts += np + [('', '', '')]

        show_table(parts)

