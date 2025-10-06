"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from typing import List

from django.contrib import admin
from django.urls import include, path
from core_utils.utils.swagger import swagger_urlpatter

urlpatterns: List = [
    path("admin/", admin.site.urls),
    path("user-config/", include("user_config.urls")),
    path("core-utils/", include("core_utils.urls")),
    path("store/", include("store.urls")),
    path("media-storage/", include("core_utils.media_storage.urls")),
    *swagger_urlpatter,
]
