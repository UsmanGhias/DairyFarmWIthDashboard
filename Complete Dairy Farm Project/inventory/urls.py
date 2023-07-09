from django.contrib import admin
from django.urls import path, include
from store.views import EditorChartView, chart
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('users/', include('users.urls')),
    path('store/', include('store.urls')),
    # path('accounts/', include('allauth.urls')),
    path('chart/', chart, name='chart'),
    path('editor-chart/', EditorChartView.as_view(), name='editor-chart'),
]
