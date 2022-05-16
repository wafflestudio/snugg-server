"""snugg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularJSONAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("doc/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path(
        "doc/swagger",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger-ui",
    ),
    path(
        "doc/redoc", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc"
    ),
    path("", include("snugg.apps.user.urls")),
    path("", include("snugg.apps.qna.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
