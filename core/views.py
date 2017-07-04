from django.shortcuts import render
from models import *
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.urlresolvers import reverse_lazy
from forms import *
from django.core.mail import send_mail
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
# Create your views here.



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
        return HttpResponseRedirect('https://knowleds-ahlan90.c9users.io/solucao/new/'+pk)
    
    context = {'form':form , 'tarefaSol':tarefaSol, 'solucaos':solucaos, 'numSolucao':numSolucao}
    
    return render(request, template_name, context)

def solucao_issue(request, pk, template_name='solucao/solucao_form.html'):
    
    """ Problema para as solucoes """
    tarefaSol = Issue.objects.get(pk=pk)
    
    """ Lista das solucoes ja cadastradas ao problema """
    solucaos = SolucaoIssue.objects.all().filter(issue=tarefaSol)
    
    numSolucao = len(solucaos)
    
    form = SolucaoIssueForm(request.POST or None, initial={'issue':tarefaSol}) 
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('https://knowleds-ahlan90.c9users.io/solucao/issue/new/'+pk)
    
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
    PESSOA
    
"""
 
@csrf_protect
def register(request, template_name='registration/register.html'):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, prefix='form')
    
        if form.is_valid():
            user1 = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            
            usuario = Usuario()
            usuario.user = user1
            usuario.save()
        
            return HttpResponseRedirect('/login')
    else:
        form = RegistrationForm(prefix='form')
        #form2 = ProjetoKnowLedsForm(prefix='form2')
    #context = {'form': form, 'form2' : form2}
    context = {'form': form}
    variables = RequestContext(request, context)
 
    return render_to_response('registration/register.html', variables,)
 
def register_success(request):
    return render_to_response('/login',)
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')



"""
    TIME
"""

@login_required
def projetoknowleds_create(request, template_name='projetoknowleds/projetoknowleds_form.html'):
    
    form = ProjetoKnowLedsForm(request.POST or None)
    if form.is_valid():
        projeto_knowleds = form.save()
        projeto_knowleds.usuarios.add(request.user)
        projeto_knowleds.nome_webhook = str.lower(str(projeto_knowleds.nome).replace(" ",""))
        projeto_knowleds.save()
        return redirect('knowleds_list')
    else :
        print('Não foi possivel salvar!')
    return render(request, template_name, {'form':form})

@login_required
def projetoknowleds_list(request, template_name='projetoknowleds/projetoknowleds_list.html'):
    
    #usuario = Usuario.objects.get(user=request.user)
    """ Lista das solucoes ja cadastradas ao problema """
    
    projetos = ProjetoKnowLeds.objects.all().filter(usuarios=request.user)

    data = {}
    data['object_list'] = projetos
    #data['usuario'] = usuario
    
    return render(request, template_name, data)


def user_create(request, pk, template_name='projetoknowleds/projetoknowleds_user.html'):
    form = IntegranteForm(request.POST or None)
    if form.is_valid():
        try:
            user = form.save(commit=False)
            user = User.objects.get(email=user.email)
            projeto = ProjetoKnowLeds.objects.get(pk=pk)
            projeto.usuarios.add(user)
            user.save()
            return redirect('knowleds_list')
        except User.DoesNotExist:
            template_name ='projetoknowleds/projetoknowleds_register.html'
            return render(request, template_name)
    return render(request, template_name, {'form':form})
