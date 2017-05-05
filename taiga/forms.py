from django.forms import ModelForm
from taiga.models import Projeto, ItemConhecimento, PessoaConhecimento, Link, Livro
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class ItemConhecimentoForm(ModelForm):
    class Meta:
        model = ItemConhecimento
        fields = ['descricao']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Usuario'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':'Password'}))


class ProjetoForm(ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome']


class TeamForm(forms.Form):
    
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email Integrante"))
    
    
class PessoaConhecimentoForm(ModelForm):
    class Meta:
        model = PessoaConhecimento
        fields = ['pessoa']


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ['url']


class LivroForm(ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'edicao']
