"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
import os
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/", include("api.urls")),
]


if os.environ.get("DEBUG") != "0" or not os.environ.get("DEBUG"):

    urlpatterns += [
        # Open API 자체를 조회 : json, yaml,
        path("json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
        path("yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
        # Open API Document UI로 조회: Swagger, Redoc
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema-json"),
            name="swagger-ui",
        ),
        path(
            "redoc/",
            SpectacularRedocView.as_view(url_name="schema-json"),
            name="redoc",
        ),
    ]