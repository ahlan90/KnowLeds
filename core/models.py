from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from taiga.models import Issue, Projeto, Task

# Create your models here.

class Usuario(models.Model):
    
    user = models.OneToOneField(User, null=True)
    email = models.EmailField()
    
    def __str__(self):
        return self.email


class ProjetoKnowLeds(models.Model):
    
    nome = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    usuarios = models.ManyToManyField(User)

    def __str__(self):
        return 'Nome: ' + self.nome + ' , Email: ' + str(self.email)
    
    def get_sprint_url(self):
        return u"/sprint/list/%i" % self.id

    def get_issue_url(self):
        return u"/issue/list/%i" % self.id

    def get_user_url(self):
        return u"/integrante/new/%i" % self.id
    
    def get_permalink(self):
        projeto = Projeto.objects.get(id=self.id)
        return projeto.permalink


class Solucao(models.Model):
    
    descricao = models.CharField(max_length=200)
    
    tarefa = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return 'Solucao[id: {id}, descricao: {descricao}]'.format(
            id=self.id, descricao=self.descricao)

    def get_solucao_new_url(self):
        return u"/solucao/new/%i" % self.id


class SolucaoIssue(models.Model):
    
    descricao = models.CharField(max_length=200)
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return 'Solucao[id: {id}, descricao: {descricao}]'.format(
            id=self.id, descricao=self.descricao)
            
    def get_solucao_new_url(self):
        return u"/solucao/issue/new/%i" % self.id
