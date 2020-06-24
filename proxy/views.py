from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from proxy.models import Document, Domain


class HomeView(TemplateView):
    template_name = 'homeview.html'

    def get_context_data(self, **kwargs):
        domains = Domain.objects.all()

        data = []
        for dom in domains:
            docs = Document.objects.filter(domain=dom)
            data += [(
                dom, docs.count()
            )]

        return {
            'data': sorted(data, key=lambda datum: datum[0].domain)
        }


class ProxyView(View):

    def get(self, request, proxy_url, *args, **kwargs):
        print('IN PROXY, ', request.get_full_path())
        if request.is_secure():
            print('SECURE REQUEST ON ', request)

        doc = Document.objects.filter(url=proxy_url)[:1]

        if len(doc) == 0:
            return render(request, 'notfound.html', {'url': proxy_url}, 404)

        doc = doc[0]
        response = HttpResponse(content_type=doc.mime)
        response.write(doc.content)

        return response
