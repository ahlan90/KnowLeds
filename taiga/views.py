from rest_framework import generics
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.urlresolvers import reverse_lazy
from taiga.forms import ProjetoForm, LoginForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from models import Sprint, Task, Issue, UserStory, Projeto
from django.core.mail import send_mail
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from core.models import ProjetoKnowLeds, Solucao, SolucaoIssue, Usuario



@login_required
def home(request):
    return render(request, template_name='index.html')
    
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def get_taiga_status(request, nomeProjeto):

    try:
        projeto_knowleds = ProjetoKnowLeds.objects.get(nome=nomeProjeto)
    except:
        pass
    
    
    if request.method == 'GET':
        return Response("GET")

    elif request.method == 'POST':
        print ('POST')
        r = json.load(request)
        if r['action'] == 'create' :
           
            # Se for SPRINT
            if r['type'] == 'milestone':
                
                projeto = projeto_save(r['data']['project'], projeto_knowleds)
                
                sprint_save(r['data'], projeto)


            # Se for USER HISTORY
            elif r['type'] == 'userstory':
                
                projeto = projeto_save(r['data']['project'], projeto_knowleds)
                
                print('ALGO MUDOU:  ' + str(r))
                
                userstory_save(r['data'],projeto)

            
            # Se for TASK
            elif r['type'] == 'task':
                
                projeto = projeto_save( r['data']['project'], projeto_knowleds)
                
                userStory = userstory_save(r['data']['user_story'], projeto)

                task = Task()
                
                
                # Atributos para salvar 
                task.ident = r['data']['id']
                task.titulo = r['data']['subject']
                task.descricao = r['data']['description']
                task.userStory = userStory
                task.tags = r['data']['tags']
                task.is_closed = r['data']['status']['is_closed']
                
                try:
                    ##identificar qual user
                    task.user = r['data']['assigned_to']['username']
                except:
                    pass
          
          
          
                textoTag = task.titulo + ' precisa de ajuda, voce sabe a solucao'
                
                """"
                    
                for tag in task.getTags():
                    if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                        print('Mandando o email...')
                        send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)
                """
                
                task.save()
            
            # Se for ISSUE
            elif r['type'] == 'issue':
                
                projeto = projeto_save(r['data']['project'], projeto_knowleds)
                
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

                
                projeto = projeto_save(r['data']['project'], projeto_knowleds)
                
                userstory_save(r['data'],projeto)
                
                
            # Se for TASK
            elif r['type'] == 'task':
                
                if Task.objects.filter(ident=r['data']['id']):
                    task = Task.objects.filter(ident=r['data']['id'])[0]
                else:
                    task = Task()
                
                
                projeto = projeto_save( r['data']['project'], projeto_knowleds)
                
                userStory = userstory_save(r['data']['user_story'], projeto)
                
                print("\n\nOlha aqui o user story: " + str(userStory))
                
                # Atributos para salvar 
                task.ident = r['data']['id']
                task.titulo = r['data']['subject']
                task.descricao = r['data']['description']
                task.userStory = userStory
                task.tags = r['data']['tags']
                task.is_closed = r['data']['status']['is_closed']
                
                try:
                    ##identificar qual user
                    task.user = r['data']['assigned_to']['username']
                except:
                    pass
            
                task.save()
                
                """
                
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

                """
                
                
            # Se for ISSUE
            elif r['type'] == 'issue':
                
                projeto = projeto_save(r['data']['project'], projeto_knowleds)
                
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

                """
                textoTag = issue.titulo + ' precisa de ajuda, voce sabe a solucao'
                
                for tag in issue.getTags():
                    if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                        print('Mandando o email...')
                        send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)

                """

                
            #Se for SPRINT
            elif r['type'] == 'milestone':
                
                projeto = projeto_save(r['data']['project'], projeto_knowleds)
                
                sprint_save(r['data'], projeto)
                
            
        return Response("POST", status=status.HTTP_201_CREATED)


"""
    PROJETO
    
"""
def projeto_create(request, template_name='projeto/projeto_form.html'):
    form = ProjetoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('projeto_integration')
    return render(request, template_name, {'form':form})


@login_required
def projeto_list(request, template_name='projeto/projeto_list.html'):
    
    usuario = Usuario.objects.get(user=request.user)
    """ Lista das solucoes ja cadastradas ao problema """
    projetos = Projeto.objects.all().filter(time=usuario.time)

    data = {}
    data['object_list'] = projetos
    data['usuario'] = usuario
    
    return render(request, template_name, data)



"""

  TASK
  
"""
def tarefa_list(request, pk, template_name='tarefa/tarefa_list.html'):
    
    """ Problema para as solucoes """
    userStory = UserStory.objects.all().filter(pk=pk)
    
    
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
    
    projeto = Projeto.objects.get(pk=pk)
    
    sprints = Sprint.objects.all().filter(projeto=projeto)
    data = {}
    data['object_list'] = sprints
    return render(request, template_name, data)



"""
    Views para ISSUE

"""

def issue_list(request, pk, template_name='issue/issue_list.html'):
    
    projeto = Projeto.objects.get(pk=pk)
    
    issues = Issue.objects.all().filter(projeto=projeto)
    
    print('Tamanho ISSUE: ' + str(len(issues)))
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
    
    print('Tamanho ' + str(len(userstory)))
    
    data = {}
    data['object_list'] = userstory
    data['sprint'] = sprintUS
    return render(request, template_name, data)




"""
    PARSERS
"""

def projeto_save(jsonLoad, projetoKnowLeds):
        
    if Projeto.objects.filter(projeto_id=jsonLoad['id']):
        projeto = Projeto.objects.filter(projeto_id=jsonLoad['id'])[0]
    else:
        projeto = Projeto()
    
    projeto.projeto_id = jsonLoad['id']
    projeto.permalink = jsonLoad['permalink']
    projeto.nome = jsonLoad['name']
    projeto.projeto_knowleds = projetoKnowLeds
    
    projeto.save()
    
    return projeto


def sprint_save(jsonLoad, meuProjeto):
    
    
    sprint = Sprint()
        
    try:
        sprint = Sprint.objects.get(ident=jsonLoad['id'])
    except:
        pass
    
    
    try:
        print("O que esta " + sprint.nome + " o que veio foi : " + jsonLoad['name'] )
    except:
        pass
    
    # Atributos para salvar 
    sprint.nome = jsonLoad['name']
    sprint.ident = jsonLoad['id']
    sprint.dataInicio = jsonLoad['estimated_start']
    sprint.dataFim = jsonLoad['estimated_finish']
    sprint.is_closed = jsonLoad['closed']
    sprint.projeto = meuProjeto
    
    sprint.save()
    
    return sprint
    

def userstory_save(jsonLoad, meuProjeto):
    
    userStory = UserStory()
    
    try:
        userStory = UserStory.objects.get(ident=jsonLoad['id'])
    except:
        pass

    
    if(jsonLoad['milestone'] != None):
        sprint = sprint_save(jsonLoad['milestone'], meuProjeto)
    else:
        sprint = None
    
    
    try:
        # Atributos para salvar 
        userStory.ident = jsonLoad['id']
        userStory.titulo = jsonLoad['subject']
        userStory.descricao = jsonLoad['description']
        userStory.setTags(jsonLoad['tags'])
        userStory.sprint = sprint
        
        """
        
        textoTag = userStory.titulo + ' precisa de ajuda, voce sabe a solucao'
        
        for tag in userStory.getTags():
            if tag == 'ajuda' or tag == 'Ajuda' or tag == 'AJUDA':
                print('Mandando o email...')
                send_mail('Ajuda em UserStory', textoTag, 'ahlan90@gmail.com', ['ahlan90@gmail.com'], fail_silently=False)
        
        """
        
        userStory.save()
        
    except Exception as e:
        print(e)
        pass
    
    return userStory