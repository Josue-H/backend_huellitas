from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsArticleViewSet, SuccessStoryViewSet, FAQViewSet

app_name = 'content'

router = DefaultRouter()
router.register(r'news', NewsArticleViewSet, basename='news')
router.register(r'success-stories', SuccessStoryViewSet, basename='success-story')
router.register(r'faqs', FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
]