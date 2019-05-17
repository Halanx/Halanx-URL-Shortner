from rest_framework import generics
from shortener.models import Url
from .serializer import URLSerializer


class URLRetrieveView(generics.RetrieveAPIView):
    lookup_field = 'short'
    serializer_class = URLSerializer
    queryset = Url.objects.all()


class URLCreateView(generics.CreateAPIView):
    lookup_field = 'short'
    serializer_class = URLSerializer
    queryset = Url.objects.all()
