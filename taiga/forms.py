from django.forms import ModelForm
from taiga.models import Projeto, Problema, Solucao, ItemConhecimento, PessoaConhecimento, Link, Livro, Usuario, ProjetoKnowLeds, SolucaoIssue
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class ProblemaForm(ModelForm):
    class Meta:
        model = Problema
        fields = ['titulo','tags','descricao']


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


class ProjetoKnowLedsForm(ModelForm):
    
    nome = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Nome Projeto"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email Projeto"))
    
    class Meta:
        model = ProjetoKnowLeds
        fields = ['nome','email']


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


class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs={ 'required' : 'True', 'max_length' : '30', 'placeholder' : 'Usuario', 'class' : 'form-control'}), label=_(""), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs={'required' : 'True', 'max_length' : '30', 'placeholder' : 'Email', 'class' : 'form-control'}), label=_(""))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'required' : 'True', 'max_length' : '30', 'placeholder' : 'Senha', 'render_value':'False', 'class' : 'form-control'}), label=_(""))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'required' : 'True', 'max_length' : '30', 'placeholder' : 'Senha (novamente)', 'render_value':'False', 'class' : 'form-control'}), label=_(""))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class IntegranteForm(ModelForm):
    
   class Meta:
       model = User
       fields = ['email']