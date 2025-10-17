from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet

app_name = 'contact'

router = DefaultRouter()
router.register(r'messages', ContactMessageViewSet, basename='contact-message')

urlpatterns = [
    path('', include(router.urls)),
]