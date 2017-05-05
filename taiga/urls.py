from django.conf.urls import url, include
from django.contrib import admin
from taiga import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


urlpatterns = [
    
    url(r'^wh/(?P<nomeProjeto>\w+)/$', views.get_taiga_status),
    
    url(r'^projeto/new$', views.projeto_create, name='projeto_new'),
    
    url(r'^projetos$', views.projeto_list, name='projeto_list'),
    
    url(r'^sprint/list/(?P<pk>\d+)$', views.sprint_list, name='sprint_list'),
    
    url(r'^tarefa/list/(?P<pk>\d+)$', views.tarefa_list, name='tarefa_list'),
    
    url(r'^userstory/list/(?P<pk>\d+)$', views.userstory_list, name='userstory_list'),
    
    url(r'^issue/list/(?P<pk>\d+)$', views.issue_list, name='issue_list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

