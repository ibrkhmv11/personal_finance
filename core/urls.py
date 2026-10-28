"""
URL configuration for core project.

3 ta tilda (uz, ru, en) ishlash imkoniyati, Swagger UI, ReDoc va
interaktiv Postman uslubidagi Web UI bilan to'liq jihozlangan URL marshrutlari.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Bosh sahifaga kirilganda to'g'ridan-to'g'ri Swagger UI (API docs) ga o'tadi
    path('', RedirectView.as_view(url='/api/docs/', permanent=False), name='swagger-home'),

    # Django boshqaruv paneli (Admin panel)
    path('admin/', admin.site.urls),

    # Django rasmiy tilni o'zgartirish (set_language) yo'li
    path('i18n/', include('django.conf.urls.i18n')),

    # Finance loyihasining asosiy REST API marshrutlari
    path('api/', include('finance.urls')),

    # Swagger / OpenAPI hujjatlari va interaktiv sinov paneli (Swagger UI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
