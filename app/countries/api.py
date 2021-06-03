from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from countries.models import Country, OriginCountry, BorderStatus
from countries.serializers import CountrySerializer, OriginCountrySerializer, BorderStatusEditorSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class BorderStatusViewSet(viewsets.ModelViewSet):
    queryset = BorderStatus.objects.all()
    serializer_class = BorderStatusEditorSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields=('origin_country','destination')

class OriginCountryViewSet(viewsets.ModelViewSet):
    queryset = OriginCountry.objects.all()
    serializer_class = OriginCountrySerializer
    #use django filter backend instead of search filter to get query bu filter fields instead of `search=`
    filter_backends = (DjangoFilterBackend,)
    filter_fields=('origin_country__name',)
