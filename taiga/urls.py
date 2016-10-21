from django.conf.urls import url, include
from django.contrib import admin
from taiga import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


urlpatterns = [
    
    url(r'^wh/(?P<nomeProjeto>\w+)/$', views.get_taiga_status),
    
    url(r'^problemas$', views.problema_list, name='problema_list'),
    
    url(r'^$', views.projetoknowleds_list, name='knowleds_list'),
    
    url(r'^problema/new$', views.problema_create, name='problema_new'),
    
    url(r'^problema/edit/(?P<pk>\d+)$', views.problema_update, name='problema_edit'),
    
    url(r'^problema/delete/(?P<pk>\d+)$', views.problema_delete, name='problema_delete'),
    
    url(r'^solucao/new/(?P<pk>\d+)$', views.solucao_create, name='solucao_new'),
    
    url(r'^solucao/issue/new/(?P<pk>\d+)$', views.solucao_issue, name='solucao_issue'),
    
    url(r'^projeto/new$', views.projeto_create, name='projeto_new'),
    
    url(r'^projetos$', views.projeto_list, name='projeto_list'),
    
    url(r'^knowleds/new$', views.projetoknowleds_create, name='knowleds_new'),
    
    url(r'^integrante/new/(?P<pk>\d+)$', views.user_create, name='integrante_new'),
    
    url(r'^sprint/list/(?P<pk>\d+)$', views.sprint_list, name='sprint_list'),
    
    url(r'^tarefa/list/(?P<pk>\d+)$', views.tarefa_list, name='tarefa_list'),
    
    url(r'^userstory/list/(?P<pk>\d+)$', views.userstory_list, name='userstory_list'),
    
    url(r'^issue/list/(?P<pk>\d+)$', views.issue_list, name='issue_list'),
    
    url('^', include('django.contrib.auth.urls')),
    
    url(r'^register/$', views.register, name='register'),
    
    url(r'^register/success/$', views.register_success),
    

]

urlpatterns = format_suffix_patterns(urlpatterns)

