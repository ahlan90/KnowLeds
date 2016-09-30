from models import Sprint, Task, Issue, UserStory, Projeto
import json


class ProjetoJSON():

    def projeto_save(jsonLoad):
        
        if Projeto.objects.filter(projeto_id=jsonLoad['id']):
            print('Entrou no recuperar BANCO    ')
            projeto = Projeto.objects.filter(projeto_id=jsonLoad['id'])[0]
        else:
            projeto = Projeto()
            
            projeto.projeto_id = jsonLoad['id']
            projeto.permalink = jsonLoad['permalink']
            projeto.nome = jsonLoad['name']
        
        projeto.save()
        
        return projeto