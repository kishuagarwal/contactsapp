from django.conf.urls import url

from .views import ContactAPIView, SearchAPIView

urlpatterns = [
    url(r'^contact/$', ContactAPIView.as_view(), name='contact-list'),
    url(r'^contact/(?P<id>[0-9]+)/', ContactAPIView.as_view(), name='contact'),
    url(r'^search/$', SearchAPIView.as_view(), name='search-contact')
]
