from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from shortener.forms import SubmitUrl
from shortener.models import Url


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
