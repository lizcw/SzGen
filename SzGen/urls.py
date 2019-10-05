"""SzGen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from szgenrest import views as app_views

router = routers.DefaultRouter()
router.register(r'study', app_views.StudyViewSet)
router.register(r'participant', app_views.ParticipantViewSet)
router.register(r'clinical', app_views.ClinicalViewSet)
router.register(r'sample', app_views.SampleViewSet)
router.register(r'dataset', app_views.DatasetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('rest-auth/', include('rest_auth.urls')),
    path('captcha/', include('captcha.urls')),
    path('session_security/', include('session_security.urls')),
    path('', include('szgenapp.urls'))
]
