"""docker_django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# from docker_django1.apps.user.web.urls import router
from rest_framework.routers import DefaultRouter

from docker_django1.apps.user.web.views.userViewSet import UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='SWAGGER TITLE',
        default_version='v1',
        description='Test description',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_INDEX_TITLE
admin.site.site_title = settings.ADMIN_SITE_TITLE

BASE_URL = 'api/v1'

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')


urlpatterns = [
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    url(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    url(
        r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'
    ),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # DRF routers
    path(f'{BASE_URL}/', include(router.urls)),
]

apps = settings.INSTALLED_APPS

try:
    import debug_toolbar

    if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
except ImportError:
    pass
