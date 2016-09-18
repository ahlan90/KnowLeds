from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
import json


# Create your models here.

class Problema(models.Model):
    
    titulo = models.CharField(max_length=200)
    tags = TaggableManager()
    descricao = models.TextField(max_length=300)
    
    
    def __str__(self):
        return 'Problema[id: {id}, descricao: {descricao}]'.format(
            id=self.id, descricao=self.descricao)
    
    def get_solucao_new_url(self):
        return u"/solucao/new/%i" % self.id


class ItemConhecimento(models.Model):
    
    descricao = models.CharField(max_length=200)
    
    def __str__(self):
        return self.descricao


class Projeto(models.Model):
    
    projeto_id = models.IntegerField()
    nome = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    permalink = models.CharField(max_length=200)
    pessoa = models.ManyToManyField(User)
    
    def __str__(self):
        return self.nome + ' Usuario: ' + str(self.pessoa.count())

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
        return self.nome + self.is_closed

    def get_userstory_url(self):
        return u"/userstory/list/%i" % self.id


class UserStory(models.Model):

    ident = models.IntegerField()
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    
    def __unicode__(self):
        return self.titulo + ', ' + str(self.sprint) + ', tags: ' + self.tags
    
    def setTags(self, x):
        self.tags = json.dumps(x)

    def getTags(self):
        return json.loads(self.tags)


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
        return 'Id: ' + str(self.ident) + ', Descricao: ' + self.descricao
    
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
    
    def __unicode__(self):
        return str(self.ident) + " " + self.descricao

    def setTags(self, x):
        self.tags = json.dumps(x)

    def getTags(self):
        return json.loads(self.tags)


class Solucao(models.Model):
    
    descricao = models.CharField(max_length=200)
    
    tarefa = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return 'Solucao[id: {id}, descricao: {descricao}]'.format(
            id=self.id, descricao=self.descricao)

    def get_solucao_new_url(self):
        return u"/solucao/new/%i" % self.id