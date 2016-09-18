from taiga.models import Solucao, Problema
# from gestao.serializers import TagSerializer, SolucaoSerializer, ProblemaSerializer
from rest_framework import generics
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.urlresolvers import reverse_lazy
from taiga.forms import ProblemaForm, SolucaoForm, ProjetoForm, LoginForm, RegistrationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from models import Sprint, Task, Issue, UserStory, Projeto
from django.core.mail import send_mail
import json
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext


@login_required
def home(request):
    return render_to_response('registration/login.html', { 'user': request.user })
    
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def get_taiga_status(request, username):
    print('AKIIII ' + username)
    try:
        usuario = User.objects.get(username=username)
        print('E do usuario: ' + usuario.username)
    except:
        pass
    
    if request.method == 'GET':
        print ('GET')
        return Response("GET")
    elif request.method == 'POST':
        print ('POST')
        r = json.load(request)
        if r['action'] == 'create' :
           
            # Se for SPRINT
            if r['type'] == 'milestone':
                
                if Projeto.objects.filter(projeto_id=r['data']['project']['id']):
                    print('Entrou no recuperar BANCO    ')
                    projeto = Projeto.objects.filter(projeto_id=r['data']['project']['id'])[0]
                else:
                    projeto = Projeto()
                    
                    projeto.projeto_id = r['data']['project']['id']
                    projeto.permalink = r['data']['project']['permalink']
                    projeto.nome = r['data']['project']['name']
                    
                    projeto.save()
                    
                    projeto.pessoa.add(usuario)
                        
                sprint = Sprint()
                
                # Atributos para salvar 
                sprint.nome = r['data']['name']
                sprint.ident = r['data']['id']
                sprint.dataInicio = r['data']['estimated_start']
                sprint.dataFim = r['data']['estimated_finish']
                sprint.is_closed = r['data']['closed']
                sprint.projeto = projeto
                
                sprint.save()
                
            # Se for USER HISTORY
            elif r['type'] == 'userstory':
                
                userStory = UserStory()
               
                
                try:
                    if(r['data']['milestone'] == None):
                        sprint = Sprint()
                        sprint.nome = r['data']['milestone']['data']['name']
                        sprint.ident = r['data']['milestone']['data']['id']
                        sprint.dataInicio = r['data']['milestone']['data']['estimated_start']
                        sprint.dataFim = r['data']['milestone']['data']['estimated_finish']
                        sprint.is_closed = r['data']['milestone']['data']['closed']
                        
                        sprint.save()
                    else:
                        sprint = Sprint.objects.get(ident=r['data']['milestone']['id'])
                        
                except:
                    pass
                
                
                try:
                    # Atributos para salvar 
                    userStory.ident = r['data']['id']
                    userStory.titulo = r['data']['subject']
                    userStory.descricao = r['data']['description']
                    userStory.setTags(r['data']['tags'])
                    
                    """try:
                        userStory.sprint = sprint
                    except:
                        pass
                    """
                    
                    textoTag = userStory.titulo + ' precisa de ajuda, voce sabe a solucao'
                    
                    for tag in userStory.getTags():
                        if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                            print('Mandando o email...')
                            send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)
                    
                    userStory.save()
                except Exception as e:
                    print e
                    pass
            
            # Se for TASK
            elif r['type'] == 'task':
                
                task = Task()
                
                
                # Atributos para salvar 
                task.ident = r['data']['id']
                task.titulo = r['data']['subject']
                task.descricao = r['data']['description']
                task.userHistory = r['data']['user_story']['id']
                task.tags = r['data']['tags']
                task.is_closed = r['data']['status']['is_closed']
                task.sprint_id = r['data']['milestone']['id']
                
                try:
                    ##identificar qual user
                    task.user = r['data']['assigned_to']['username']
                except:
                    pass
          
          
                textoTag = task.titulo + ' precisa de ajuda, voce sabe a solucao'
                    
                for tag in task.getTags():
                    if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                        print('Mandando o email...')
                        send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)

                task.save()
            
            # Se for ISSUE
            elif r['type'] == 'issue':
                
                if Projeto.objects.filter(projeto_id=r['data']['project']['id']) :
                    print('Entrou no recuperar BANCO    ')
                    projeto = Projeto.objects.filter(projeto_id=r['data']['project']['id'])
                else:
                    projeto = Projeto()
                    projeto.projeto_id = r['data']['project']['id']
                    projeto.permalink = r['data']['project']['permalink']
                    projeto.nome = r['data']['project']['name']
                    projeto.pessoa.add(usuario)
                
                    projeto.save()
                
                issue = Issue()
                
                # Atributos para salvar 
                issue.ident = r['data']['id']
                issue.titulo = r['data']['subject']
                issue.descricao = r['data']['description']
                issue.tags = r['data']['description']
                issue.is_closed = r['data']['status']['is_closed']
                issue.projeto = projeto
      
                issue.save()
                

        elif r['action'] == 'change':
            
            
             # Se for USER HISTORY
            if r['type'] == 'userstory':
                
                userStory = UserStory()
                
                try:
                    
                    try:
                        sprint = Sprint.objects.get(ident=r['data']['milestone']['id'])
                    except:
                        sprint = Sprint()
                        pass
                    
                    # Atributos para salvar quit
                    sprint.nome = r['data']['milestone']['name']
                    sprint.ident = r['data']['milestone']['id']
                    sprint.dataInicio = r['data']['milestone']['estimated_start']
                    sprint.dataFim = r['data']['milestone']['estimated_finish']
                    sprint.is_closed = r['data']['milestone']['closed']
                    sprint.projeto_id = r['data']['milestone']['project']['id']
                    
                    sprint.save()
                except:
                    pass
                
                try:
                    
                    try:
                        userStory = UserStory.objects.get(ident=r['data']['id'])
                    except:
                        userStory = UserStory()
                        pass
                    
                    # Atributos para salvar 
                    userStory.ident = r['data']['id']
                    userStory.titulo = r['data']['subject']
                    userStory.descricao = r['data']['description']
                    userStory.setTags(r['data']['tags'])
                    userStory.sprint = sprint
                    userStory.save()
                    
                    textoTag = userStory.titulo + ' precisa de ajuda, voce sabe a solucao'
                    
                    for tag in userStory.getTags():
                        if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                            print('Mandando o email...')
                            send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)
                        
                except Exception as e:
                    print e
                    pass
                
            # Se for TASK
            elif r['type'] == 'task':
                
                
                
                try:
                    task = Task.objects.get(ident=r['data']['id'])
                except:
                    task = Task()
                    pass
                
                # Atributos para salvar 
                task.ident = r['data']['id']
                task.titulo = r['data']['subject']
                task.descricao = r['data']['description']
                task.userHistory = r['data']['user_story']['id']
                task.tags = r['data']['tags']
                task.is_closed = r['data']['status']['is_closed']
                task.sprint_id = r['data']['milestone']['id']
                
                try:
                    ##identificar qual user
                    task.user = r['data']['assigned_to']['username']
                except:
                    pass
            
                task.save()
                
                texto = ''
                
                
                for t in Task.objects.all().filter(sprint_id=r['data']['milestone']['id']):
                    texto += 'Tarefa: ' + t.titulo + ': \n' + 'Descricao: '+ t.descricao + '\n \n \n'
                
                
                # Se a tarefa encerrar o Sprint entra aqui
                # para ENVIAR o EMAIL
                
                email = Projeto.objects.get(nomeFantasia = 'Teste').email
                
                print('Olha como esta o status: ' + str(r['data']['milestone']['closed']))
                
                if r['data']['milestone']['closed']:
                    sprint = 'O Sprint: ' + r['data']['milestone']['name'] + ' foi encerrado'
                    send_mail(sprint, texto, 'paulossjunior@gmail.com, ahlan90@gmail.com,', [email], fail_silently=False)
            
                textoTag = task.titulo + ' precisa de ajuda, voce sabe a solucao'
                
                for tag in task.getTags():
                    if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                        print('Mandando o email...')
                        send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)

            # Se for ISSUE
            elif r['type'] == 'issue':
                
                if Projeto.objects.filter(projeto_id=r['data']['project']['id']) :
                    print('Entrou no recuperar BANCO    ')
                    projeto = Projeto.objects.filter(projeto_id=r['data']['project']['id'])
                else:
                    projeto = Projeto()
                    
                projeto.projeto_id = r['data']['project']['id']
                projeto.permalink = r['data']['project']['permalink']
                projeto.nome = r['data']['project']['name']
                
                projeto.save()
                
                projeto.pessoa.add(usuario)
                
                projeto.save()
                
                try:
                    issue = Issue.objects.get(ident=r['data']['id'])
                except:
                    issue = Issue()
                    pass
                
                issue.ident = r['data']['id']
                issue.titulo = r['data']['subject']
                issue.descricao = r['data']['description']
                issue.tags = r['data']['description']
                issue.is_closed = r['data']['status']['is_closed']
                issue.projeto = projeto
                
                issue.save()

                textoTag = issue.titulo + ' precisa de ajuda, voce sabe a solucao'
                
                for tag in issue.getTags():
                    if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                        print('Mandando o email...')
                        send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)

            elif r['type'] == 'milestone':
                
                if Projeto.objects.filter(projeto_id=r['data']['project']['id']) :
                    print('Entrou no recuperar BANCO    ')
                    projeto = Projeto.objects.filter(projeto_id=r['data']['project']['id'])[0]
                else:
                    projeto = Projeto()
                    
                projeto.projeto_id = r['data']['project']['id']
                projeto.permalink = r['data']['project']['permalink']
                projeto.nome = r['data']['project']['name']
                
                
                projeto.save()
                
                projeto.pessoa.add(usuario)
                
                projeto.save()
                
                sprint = Sprint()
            
                try:
                    sprint = Sprint.objects.get(ident=r['data']['id'])
                except:
                    pass
                
                # Atributos para salvar 
                sprint.nome = r['data']['name']
                sprint.ident = r['data']['id']
                sprint.dataInicio = r['data']['estimated_start']
                sprint.dataFim = r['data']['estimated_finish']
                sprint.is_closed = r['data']['closed']
                sprint.projeto = projeto
                
                sprint.save()
            
        return Response("POST", status=status.HTTP_201_CREATED)


"""
    Views para PROBLEMA

"""

def problema_list(request, template_name='problema/problema_list.html'):
    problemas = Problema.objects.all()
    data = {}
    data['object_list'] = problemas
    return render(request, template_name, data)

def problema_create(request, template_name='problema/problema_form.html'):
    form = ProblemaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('problema_list')
    return render(request, template_name, {'form':form})

def problema_update(request, pk, template_name='problema/problema_form.html'):
    problema = get_object_or_404(Problema, pk=pk)
    form = ProblemaForm(request.POST or None, instance=problema)
    if form.is_valid():
        form.save()
        return redirect('problema_list')
    return render(request, template_name, {'form':form})

def problema_delete(request, pk, template_name='problema/problema_confirm_delete.html'):
    problema = get_object_or_404(Problema, pk=pk)    
    if request.method=='POST':
        problema.delete()
        return redirect('problema_list')
    return render(request, template_name, {'object':problema})



"""
    Views para SOLUCAO

"""


def solucao_list(request, template_name='solucao/solucao_list.html'):
    solucaos = Solucao.objects.all()
    data = {}
    data['object_list'] = solucaos
    return render(request, template_name, data)

def solucao_create(request, pk, template_name='solucao/solucao_form.html'):
    
    """ Problema para as solucoes """
    tarefaSol = Task.objects.get(pk=pk)
    
    """ Lista das solucoes ja cadastradas ao problema """
    solucaos = Solucao.objects.all().filter(tarefa=tarefaSol)
    
    numSolucao = len(solucaos)
    
    form = SolucaoForm(request.POST or None, initial={'tarefa':tarefaSol}) 
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('https://knowleds-ahlan90.c9users.io/solucao/new/2')
    
    context = {'form':form , 'tarefaSol':tarefaSol, 'solucaos':solucaos, 'numSolucao':numSolucao}
    
    return render(request, template_name, context)

def solucao_update(request, pk, template_name='solucao/solucao_form.html'):
    solucao = get_object_or_404(Solucao, pk=pk)
    form = SolucaoForm(request.POST or None, instance=solucao)
    if form.is_valid():
        form.save()
        return redirect('solucao_list')
    return render(request, template_name, {'form':form})

def solucao_delete(request, pk, template_name='solucao/solucao_confirm_delete.html'):
    solucao = get_object_or_404(Solucao, pk=pk)    
    if request.method=='POST':
        solucao.delete()
        return redirect('solucao_list')
    return render(request, template_name, {'object':solucao})



"""
    PROJETO
    
"""
def projeto_create(request, template_name='projeto/projeto_form.html'):
    form = ProjetoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('projeto_integration')
    return render(request, template_name, {'form':form})


def projeto_list(request, template_name='projeto/projeto_list.html'):
    
    """ Lista das solucoes ja cadastradas ao problema """
    projetos = Projeto.objects.all().filter(pessoa=request.user)

    data = {}
    data['object_list'] = projetos
    
    return render(request, template_name, data)


"""

  TASK
  
"""
def tarefa_list(request, pk, template_name='tarefa/tarefa_list.html'):
    
    """ Problema para as solucoes """
    userStory = UserStory.objects.get(pk=pk)
    
    
    """ Lista das solucoes ja cadastradas ao problema """
    tarefas = Task.objects.all().filter(userStory=userStory)

    for tarefaX in tarefas:
        tarefaX.numeroSolucoes = len(Solucao.objects.all().filter(tarefa=tarefaX))
    
    data = {}
    data['object_list'] = tarefas
    
    return render(request, template_name, data)
    
def get_json_atribute(atributo, atributo_json):
    if atributo_json is not None:
        atributo = atributo_json



"""
    Views para SPRINTS

"""

def sprint_list(request, pk, template_name='sprint/sprint_list.html'):
    
    sprints = Sprint.objects.all().filter(pk=pk)
    data = {}
    data['object_list'] = sprints
    return render(request, template_name, data)


"""
    Views para ISSUE

"""

def issue_list(request, pk, template_name='issue/issue_list.html'):
    
    issues = Issue.objects.all().filter(pk=pk)
    data = {}
    data['object_list'] = issues
    return render(request, template_name, data)



"""
    Views para USER STORYS

"""


def userstory_list(request, pk, template_name='userstory/userstory_list.html'):
    
    """ Problema para as solucoes """
    sprintUS = Sprint.objects.get(pk=pk)
    
    print('Testeeeee :' + sprintUS.nome) 
    
    """ Lista das solucoes ja cadastradas ao problema """
    userstory = UserStory.objects.all().filter(sprint=sprintUS)
    
    data = {}
    data['object_list'] = userstory
    data['sprint'] = sprintUS
    return render(request, template_name, data)



"""
    PESSOA
    
"""
 
@csrf_protect
def register(request, template_name='registration/register.html'):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
 
    return render_to_response('registration/register.html', variables,)
 
def register_success(request):
    return render_to_response('registration/success.html',)
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
