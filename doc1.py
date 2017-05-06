## Notações da API Django Rest Framework
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def get_taiga_status(request, nomeProjeto):

    try:
        # Linka o projeto do Taiga com o projeto Knowleds
        projeto_knowleds = ProjetoKnowLeds.objects.get(nome_webhook=nomeProjeto)
    except:
        pass
    
    if request.method == 'POST':
        ## Captura o JSON enviado pelo Taiga
        r = json.load(request)
        ## Identifica a action enviada pelo Taiga
        if r['action'] == 'create' :
            # Se for SPRINT
            if r['type'] == 'milestone':
                ## Executa o parse de Projeto e Salva
                projeto = projeto_save(r['data']['project'], projeto_knowleds)
                ## Salva o Sprint
                sprint_save(r['data'], projeto)


## Converte os atributos do JSON para os atributos da classe e salva
def projeto_save(jsonLoad, projetoKnowLeds):
    # Pesquisa no banco se já existe o projeto salvo
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