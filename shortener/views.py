from decouple import config
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from shortener.forms import SubmitUrl
from shortener.models import Url
from utility.url_utils import build_url
import urllib.parse


def redirect_view(request, shortcode=None):
    try:
        url_obj = Url.objects.get(short=shortcode)
        url_obj.count += 1
        url_obj.save()
        return HttpResponseRedirect(url_obj.url)
    except Url.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'URL does not exist')
        return render(request, 'home.html')


def qr_code_view(request, shortcode=None):
    try:
        url_obj = Url.objects.get(short=shortcode)
        return HttpResponse(url_obj.get_qr_code(), content_type='image/png')
    except Url.DoesNotExist:
        return JsonResponse({'error': 'URL does not exist'}, status=500)


class HomeView(View):
    @staticmethod
    def get(request):
        form = SubmitUrl()
        context = {
            "title": "Submit URL",
            "form": form
        }
        return render(request, 'home.html', context)

    @staticmethod
    def post(request):
        form = SubmitUrl(request.POST)
        context = {
            "title": "Submit URL",
            "form": form
        }
        if form.is_valid():
            current_url = form.cleaned_data.get('url')
            custom_short_code = form.cleaned_data.get('short_code')
            obj = None
            if custom_short_code:
                if Url.objects.filter(short=custom_short_code).exists():
                    context = {
                        'title': 'Failed to shorten URL :(',
                        'error': 'Custom short code already taken.'
                    }
                else:
                    obj, created = Url.objects.get_or_create(url=current_url, short=custom_short_code)
            else:
                obj, created = Url.objects.get_or_create(url=current_url)

            if obj:
                context = {
                    'title': 'URL Shortened!',
                    'object': obj,
                }
            return render(request, 'result.html', context)

        return render(request, 'home.html', context)


class AffiliateQRManageView(View):
    @staticmethod
    def get(request):
        if request.GET.get('code'):
            shortcode = request.GET['code']
            url_obj = Url.objects.filter(short=shortcode).first()
            if url_obj:
                params = urllib.parse.parse_qs(urllib.parse.urlparse(url_obj.url).query)
            else:
                params = None
            return render(request, 'affiliate.html', {'url_obj': url_obj, 'code': shortcode, 'params': params,
                                                      'GOOGLE_MAPS_API_KEY': config('GOOGLE_MAPS_API_KEY')})
        return render(request, 'affiliate.html')

    @staticmethod
    def post(request):
        data = request.POST
        shortcode = data.get('code')
        affiliate_unique_code = data.get('affiliate_unique_code')
        latitude = data.get('lat')
        longitude = data.get('lng')

        url_obj = Url.objects.get(short=shortcode)
        url = "https://halanx.com/find-my-dream-home?ref_id={}&lat={}&lng={}".format(affiliate_unique_code,
                                                                                     latitude, longitude)
        url_obj.url = url
        url_obj.save()
        return redirect(request.path + "?" + urllib.parse.urlencode({'code': shortcode}))
