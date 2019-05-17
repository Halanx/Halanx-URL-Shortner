import random
import string

from django.conf import settings
from django.db import models, IntegrityError
from django.urls import reverse

from utility.qrcode_utils import generate_qr_code
from .validators import valid_url

SHORT_URL_DOMAIN = settings.SHORT_URL_DOMAIN


def b62_encode(number):
    base = string.digits + string.ascii_letters
    assert number >= 0
    if number == 0:
        return '0'
    base62 = []
    while number != 0:
        number, i = divmod(number, 62)
        base62.append(base[int(i)])
    return ''.join(reversed(base62))


def code_generator(size=6, chars=string.ascii_letters + string.digits):
    new_code = ''
    for i in range(size):
        new_code += random.choice(chars)
    return new_code


def create_shortcode(instance):
    data = instance.__class__
    try:
        last = data.objects.latest('id')
        new_code = b62_encode(last.id + int(last.created.timestamp()) % 1e5)
    except data.DoesNotExist:
        new_code = b62_encode(0)
    return new_code


class UrlManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(UrlManager, self).all(*args, **kwargs)
        qs.filter(active=True)
        return qs


class Url(models.Model):
    url = models.CharField(max_length=3000000, validators=[valid_url], blank=True, null=True)
    short = models.CharField(max_length=255, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    count = models.IntegerField(default=0)

    objects = UrlManager

    def save(self, *args, **kwargs):
        while 1:
            try:
                if self.short is None or self.short == '':
                    self.short = create_shortcode(self)
                super(Url, self).save(*args, **kwargs)
                break
            except IntegrityError:
                self.short = None
                pass

    def get_short_url(self):
        url_path = reverse("redirect", kwargs={'shortcode': self.short})
        url_path = SHORT_URL_DOMAIN + url_path
        return url_path

    def get_qr_code(self):
        return generate_qr_code(self.get_short_url()).getvalue()

    def __str__(self):
        return str(self.url)
