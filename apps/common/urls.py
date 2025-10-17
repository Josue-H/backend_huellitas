from django.urls import path
from .views import dashboard_statistics, quick_stats

app_name = 'common'

urlpatterns = [
    path('dashboard/statistics/', dashboard_statistics, name='dashboard-statistics'),
    path('dashboard/quick-stats/', quick_stats, name='quick-stats'),
]