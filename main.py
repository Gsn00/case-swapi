import functions_framework
from flask import jsonify
import requests
import time

# Cache simples em memória
CACHE = {
    'planets': {'data': None, 'timestamp': None}
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
        return call_path_planets(path, args)

## Função para tratar requisições na rota /planets
def call_path_planets(path, args):
    fetch_all('planets')  # Atualiza o cache se necessário
    all_planets = CACHE['planets']['data']
    parts = path.split('/')

    ## /planets
    if len(parts) == 2:
        ## Verifica se há parâmetros de consulta
        if args == {}:
            count = len(all_planets)
            return jsonify(paginate(all_planets, int(args.get('page', 1)), count))
        else:
            name = args.get('name', '').lower()
            terrain = args.get('terrain', '').lower()
            climate = args.get('climate', '').lower()

            filtered_planets = []

            ## Lógica para aplicar multiplos filtros
            for planet in all_planets:
                if (name in planet['name'].lower() and
                    terrain in planet['terrain'].lower() and
                    climate in planet['climate'].lower()):
                    filtered_planets.append(planet)

            count = len(filtered_planets)

            return jsonify(paginate(filtered_planets, int(args.get('page', 1)), count))
    
    ## /planets/<id>
    elif len(parts) == 3 :
        try:
            planet_id = int(parts[2])
            return jsonify(all_planets[planet_id - 1])
        except (ValueError, IndexError):
            return jsonify({'error': 'Nao encontrado.'}), 404

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