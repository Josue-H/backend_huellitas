from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdoptionApplicationViewSet, 
    SimplifiedAdoptionRequestViewSet,
    download_adoption_form
)

app_name = 'adoptions'

router = DefaultRouter()
router.register(r'applications', AdoptionApplicationViewSet, basename='adoption-application')
router.register(r'simplified', SimplifiedAdoptionRequestViewSet, basename='simplified-adoption')

urlpatterns = [
    path('download-form/', download_adoption_form, name='download-form'),
    path('', include(router.urls)),
]