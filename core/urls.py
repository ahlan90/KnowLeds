from django.conf.urls import url, include
from django.contrib import admin
from core import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


urlpatterns = [
    
    
    url(r'^$', views.projetoknowleds_list, name='knowleds_list'),
    
    url(r'^solucao/new/(?P<pk>\d+)$', views.solucao_create, name='solucao_new'),
    
    url(r'^solucao/issue/new/(?P<pk>\d+)$', views.solucao_issue, name='solucao_issue'),
    
    url(r'^knowleds/new$', views.projetoknowleds_create, name='knowleds_new'),
    
    url(r'^integrante/new/(?P<pk>\d+)$', views.user_create, name='integrante_new'),
    
    url('^', include('django.contrib.auth.urls')),
    
    url(r'^register/$', views.register, name='register'),
    
    url(r'^register/success/$', views.register_success),
    

]

urlpatterns = format_suffix_patterns(urlpatterns)

