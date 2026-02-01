import functions_framework
from flask import jsonify
import requests
import time

# Cache simples em memória
CACHE = {
    'planets': {'data': None, 'timestamp': None},
    'people': {'data': None, 'timestamp': None},
    'films': {'data': None, 'timestamp': None},
    'starships': {'data': None, 'timestamp': None},
}

TIMESTAMP_CACHE = 600  # 10 minutos em segundos

SWAPI = 'https://swapi.dev/api/'

@functions_framework.http
def hello_http(request):
    method = request.method

    ## Caso o método HTTP seja diferente de GET, ele irá retornar um erro.
    if method != 'GET':
        return jsonify({'error': 'Metodo nao permitido.'}), 405

    path = request.path
    args = request.args

    ## Rota de verificação de status
    if path == '/' or path == '':
        return jsonify({'status': 'Ok'})
    
    ## Rota para buscar planetas
    if path.startswith('/planets'):
        return handle_path('planets', path, args)
    if path.startswith('/people'):
        return handle_path('people', path, args)
    if path.startswith('/films'):
        return handle_path('films', path, args)
    if path.startswith('/starships'):
        return handle_path('starships', path, args)

## Função para tratar requisições na rota /planets
def handle_path(route, path, args):
    fetch_all(route)  # Atualiza o cache se necessário
    all_data = CACHE[route]['data']
    parts = path.split('/')

    ## Verifica se o path tem apenas um caminho, como: /planets, /characters, etc.
    if len(parts) == 2:
        ## Verifica se há parâmetros de consulta
        if args == {}:
            count = len(all_data)
            return jsonify(paginate(all_data, int(args.get('page', 1)), count))
        else:
            filtered_data = []

            match route:
                case 'planets':
                    filter_planets(filtered_data, all_data, args)
                case 'people':
                    filter_people(filtered_data, all_data, args)
                case 'films':
                    filter_films(filtered_data, all_data, args)
                case 'starships':
                    filter_starships(filtered_data, all_data, args)

            count = len(filtered_data)
            return jsonify(paginate(filtered_data, int(args.get('page', 1)), count))
    
    ## Verifica se o path tem três partes, como: /planets/1 ou /people/5...
    elif len(parts) == 3 :
        try:
            data_id = int(parts[2])
            data = None

            ## Busca o item pelo ID na lista de dados
            for item in all_data:
                if item['url'].endswith(f'/{route}/{data_id}/'):
                    data = item
                    break
                
            if data:
                return jsonify(data)
            else:
                return jsonify({'error': 'Recurso nao encontrado.'}), 404
        except (ValueError, IndexError):
            return jsonify({'error': 'ID invalido.'}), 400

## Função para filtrar planetas com base em nome, terreno e clima
def filter_planets(filtered_data, all_data, args):
    arg_name = args.get('name', '').lower()
    arg_terrain = args.get('terrain', '').lower()
    arg_climate = args.get('climate', '').lower()

    ## Lógica para aplicar multiplos filtros
    for data in all_data:
        if (arg_name in data['name'].lower() and
            arg_terrain in data['terrain'].lower() and
            arg_climate in data['climate'].lower()):
            filtered_data.append(data)

## Função para filtrar pessoas com base em nome, gênero e filme
def filter_people(filtered_data, all_data, args):
    arg_name = args.get('name', '').lower()
    arg_gender = args.get('gender', '').lower()
    arg_film = args.get('film', '').lower()

    ## Lógica para aplicar multiplos filtros
    for data in all_data:
        if (arg_name in data['name'].lower() and
            arg_gender in data['gender'].lower()):

            ## Filtra por filme se o parâmetro for fornecido
            if arg_film:
                for f in data['films']:
                    if f.endswith(f'/films/{arg_film}/'):
                        filtered_data.append(data)
                        break
            else:
                filtered_data.append(data)

## Função para filtrar filmes com base em título, personagem e ano de lançamento
def filter_films(filtered_data, all_data, args):
    arg_title = args.get('title', '').lower()
    arg_character = args.get('character', '').lower()
    arg_year = args.get('year', '').lower()

    ## Lógica para aplicar multiplos filtros
    for data in all_data:
        if (arg_title in data['title'].lower() and
            arg_year in data['release_date'].lower()):
            
            ## Filtra por personagem se o parâmetro for fornecido
            if arg_character:
                for c in data['characters']:
                    if c.endswith(f'/people/{arg_character}/'):
                        filtered_data.append(data)
                        break
            else:
                filtered_data.append(data)

## Função para filtrar naves espaciais com base em nome, modelo e piloto
def filter_starships(filtered_data, all_data, args):
    arg_name = args.get('name', '').lower()
    arg_model = args.get('model', '').lower()
    arg_pilot = args.get('pilot', '').lower()

    ## Lógica para aplicar multiplos filtros
    for data in all_data:
        if (arg_name in data['name'].lower() and
            arg_model in data['model'].lower()):

            ## Filtra por piloto se o parâmetro for fornecido
            if arg_pilot:
                for p in data['pilots']:
                    if p.endswith(f'/people/{arg_pilot}/'):
                        filtered_data.append(data)
                        break
            else:
                filtered_data.append(data)

## Função para buscar todos os dados de um recurso e armazenar em cache
def fetch_all(resource):
    ## Verifica se o cache está vazio
    if CACHE[resource]['data'] is None:
        all_data = []
        url = SWAPI + resource + '/'
        while url:
            response = requests.get(url)
            data = response.json()
            all_data.extend(data.get('results', []))
            url = data.get('next')
        CACHE[resource]['data'] = all_data
        CACHE[resource]['timestamp'] = time.time()
        print(f"Cache de {resource} populado pela primeira vez.")

    ## Verifica se o cache expirou
    elif time.time() - CACHE[resource]['timestamp'] > TIMESTAMP_CACHE:
        all_data = []
        url = SWAPI + resource + '/'
        while url:
            response = requests.get(url)
            data = response.json()
            all_data.extend(data.get('results', []))
            url = data.get('next')
        CACHE[resource]['data'] = all_data
        CACHE[resource]['timestamp'] = time.time()
        print(f"Cache de {resource} atualizado.")

## Função para paginar os dados e retornar links para próximas páginas e anteriores
def paginate(data, page, count):
    items_per_page = 10
    start = (page - 1) * items_per_page
    end = page * items_per_page

    next_page = None
    previous_page = None

    if end < len(data):
        next_page = page + 1
    if start > 0:
        previous_page = page - 1

    data = data[start:end]

    return {
        'count': count,
        'results': data,
        'next_page': '?page=' + str(next_page) if next_page else None,
        'previous_page': '?page=' + str(previous_page) if previous_page else None
    }