import httplib, urllib
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def index(request):
    url = urlparse(settings.SNOXY_HOST)

    if url.scheme=='http':
        conn = httplib.HTTPConnection(url.hostname, url.port)
    elif url.scheme=='https':
        conn = httplib.HTTPSConnection(url.hostname, url.port)

    if request.GET:
        path = '%s?%s' % (request.path, urllib.urlencode(request.GET))
    else:
        path = request.path

    conn.request(request.method, path, request.body)

    response = conn.getresponse()

    ct = response.getheader('Content-Type')
    content = response.read()

    if 'text/html' in ct:
        content = content.replace(settings.SNOXY_HOST, '')

    proxy_response = HttpResponse(
        content,
        content_type=response.getheader('Content-Type'),
        status=response.status,
        reason=response.reason
    )
    
    headers = response.getheaders()

    for k, v in headers:
        if k in ['location', 'set-cookie', 'date', 'cache-control', 'content-type']:
            proxy_response[k] = v.replace(settings.SNOXY_HOST, '')

    return proxy_response
