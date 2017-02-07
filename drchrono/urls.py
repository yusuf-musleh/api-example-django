from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^login_page/', views.login_page, name='login_page'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^send_wishes/', views.send_wishes, name='send_wishes'),

]
