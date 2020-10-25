from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('search/index.html')
    # return HttpResponse(message)
    return HttpResponse(template.render(request=request))

def mentions(request):
    template = loader.get_template('search/mentions.html')
    return HttpResponse(template.render(request=request))
