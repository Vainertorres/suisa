"""suisa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('cnf.urls', namespace='config')),
    path('sint/', include('sint.urls', namespace='sint')),
    path('den/', include('den.urls', namespace='den')),    
    path('cvd/', include('cvd.urls', namespace='cvd')),
    path('bai/', include('bai.urls', namespace='bai')), #Rips
    path('lab/', include('lab.urls', namespace='lab')),
    path('mlr/', include('mlr.urls', namespace='mlr')),
    path('sam/', include('sam.urls', namespace='sam')),    
    path('pai/', include('pai.urls', namespace='pai')),    
    path('aseg/', include('aseg.urls', namespace='aseg')),
    path('admin/', admin.site.urls),
    

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
