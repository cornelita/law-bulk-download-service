"""bd_service URL Configuration

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
from django.contrib import admin
from django.urls import path

from bd_service.views.bulk_download import BulkDownloadAllView
from bd_service.views.bulk_download import BulkDownloadView
from bd_service.views.rq import requeue_jobs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bulk-download/', BulkDownloadView.as_view(), name='bulk_download'),
    path('bulk-download/all/', BulkDownloadAllView.as_view(),
         name='bulk_download_all'),
    path('rq/requeue/', requeue_jobs),
]
