from django.forms import ModelForm
from taiga.models import Solucao, SolucaoIssue
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SolucaoForm(ModelForm):
    class Meta:
        model = Solucao
        widgets = {
            'tarefa' : forms.HiddenInput()
        }
        fields = ['tarefa' , 'descricao']


class SolucaoIssueForm(ModelForm):
    class Meta:
        model = SolucaoIssue
        widgets = {
            'issue' : forms.HiddenInput()
        }
        fields = ['issue' , 'descricao']

class ProjetoKnowLedsForm(ModelForm):
    
    nome = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Nome Projeto"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email Projeto"))
    
    class Meta:
        model = ProjetoKnowLeds
        fields = ['nome','email']