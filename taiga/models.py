from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User, UserManager, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

import json


# Create your models here.

class ItemConhecimento(models.Model):
    
    descricao = models.CharField(max_length=200)
    
    def __str__(self):
        return self.descricao


class Projeto(models.Model):

    projeto_id = models.IntegerField()
    nome = models.CharField(max_length=200)
    permalink = models.CharField(max_length=200)
    projeto_knowleds = models.OneToOneField('core.ProjetoKnowLeds', null=True)
    
    
    def __str__(self):
        return self.nome + ' ,Time: ' + str(self.projeto_knowleds)

    def get_sprint_url(self):
        return u"/sprint/list/%i" % self.id

    def get_issue_url(self):
        return u"/issue/list/%i" % self.id


class PessoaConhecimento(ItemConhecimento):
    pessoa = models.CharField(max_length=200)
    
    def __str__(self):
        return self.pessoa


class Link(ItemConhecimento):
    url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.url


class Livro(ItemConhecimento):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editora = models.CharField(max_length=200)
    edicao = models.CharField(max_length=200)
    
    def __str__(self):
        return self.titulo


class Sprint(models.Model):
    
    ident = models.IntegerField()
    nome = models.CharField(max_length=200)
    dataInicio = models.DateTimeField(blank=True, null=True) 
    dataFim = models.DateTimeField(blank=True, null=True)
    is_closed = models.CharField(max_length=200)
    projeto = models.ForeignKey(Projeto, null=True)
    
    
    def __unicode__(self):
        return self.nome + ', Finalizado: ' + self.is_closed

    def get_userstory_url(self):
        return u"/userstory/list/%i" % self.id


class UserStory(models.Model):

    ident = models.IntegerField()
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200, null=True)
    tags = models.CharField(max_length=200)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    
    
    def __unicode__(self):
        return  self.titulo + " - " + str(self.ident)
        
    
    def setTags(self, x):
        self.tags = json.dumps(x)

    def getTags(self):
        return json.loads(self.tags)
    
    def get_tarefas_url(self):
        return u"/tarefa/list/%i" % self.id


class Task(models.Model):
    
    ident = models.IntegerField()
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    userStory = models.ForeignKey(UserStory, on_delete=models.CASCADE, null=True)
    tags = models.CharField(max_length=200)
    is_closed = models.BooleanField()
    
    numeroSolucoes = models.IntegerField(null=True)
            
    ##identificar qual user
    user = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return 'Titulo: ' + self.titulo + ' userStory:' + str(self.userStory)
    
    def setTags(self, x):
        self.tags = json.dumps(x)

    def getTags(self):
        return json.loads(self.tags)
    
    def get_solucao_new_url(self):
        return u"/solucao/new/%i" % self.id


class Issue(models.Model):
    
    ident = models.IntegerField()
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    is_closed = models.BooleanField()
    projeto = models.ForeignKey(Projeto, null=True)
    
    numeroSolucoes = models.IntegerField(null=True)
    
    def __unicode__(self):
        return str(self.projeto) + " " + self.descricao

    def setTags(self, x):
        self.tags = json.dumps(x)

    def getTags(self):
        return json.loads(self.tags)

    def get_solucao_new_url(self):
        return u"/solucao/issue/new/%i" % self.id


