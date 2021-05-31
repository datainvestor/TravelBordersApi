from django.urls import include, path

from rest_framework import routers

from countries.api import CountryViewSet, OriginCountryViewSet, BorderStatusViewSet

router = routers.DefaultRouter()

router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'originlist', OriginCountryViewSet, basename='originlist')
router.register(r'borderstatus', BorderStatusViewSet, basename='borderstatus')
urlpatterns = [
    path('', include(router.urls))
]
