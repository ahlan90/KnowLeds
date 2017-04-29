from django.contrib import admin
from .models import Projeto
from .models import ItemConhecimento
from .models import Problema
from .models import PessoaConhecimento
from .models import Link
from .models import Livro

# Register your models here.
admin.site.register(ItemConhecimento)
admin.site.register(Problema)
admin.site.register(Projeto)
admin.site.register(PessoaConhecimento)
admin.site.register(Link)
admin.site.register(Livro)
