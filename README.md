# API Star Wars Otimizada para o Case PowerOfData

Este projeto foi desenvolvido como parte do processo seletivo para Desenvolvedor Back End Python na PowerOfData. Apresenta uma API Python, implementada como Google Cloud Function, focada em otimização e eficiência para consulta de dados da API pública do Star Wars (SWAPI).

## Link da API no Cloud Functions

A API está disponível e pode ser acessada através do seguinte endpoint:

`https://case-swapi-742136354522.southamerica-east1.run.app/`

## Principais Funcionalidades

*   **Filtragem Múltipla**: Permite filtrar recursos (planetas, personagens, filmes, naves) usando múltiplos parâmetros via query params, com lógica de negócio isolada e reutilizável.
*   **Paginação Manual**: Implementa paginação para gerenciar grandes volumes de dados, retornando metadados de navegação para facilitar a exploração dos resultados.
*   **Cache em Memória com TTL**: Utiliza um cache em memória com Tempo de Vida (TTL) de 10 minutos para reduzir chamadas externas à SWAPI, otimizando a performance e a latência.
*   **Atualização Automática do Cache**: O cache é automaticamente atualizado após a expiração ou se os dados não existirem, garantindo que as informações sejam sempre recentes.
*   **Transformação de Dados (DTO)**: Converte os dados brutos da SWAPI em um formato resumido e padronizado (DTO), enviando apenas informações essenciais e reduzindo o payload da resposta.
*   **Separação de Responsabilidades**: A arquitetura é modular, com cada componente (roteamento, tratamento de caminhos, busca de dados, filtragem, paginação, transformação) tendo uma função clara e bem definida, o que facilita a manutenção e escalabilidade.

## Endpoints e Filtros Disponíveis

A API oferece acesso aos seguintes recursos da SWAPI, com suporte a busca por ID, filtragem e paginação. Para todos os endpoints, a paginação pode ser controlada pelo parâmetro `page`.

### 1. `/planets`

*   **Busca por ID**: `/planets/{id}`
*   **Filtros via Query Params**:
    *   `name`: Filtra planetas pelo nome (busca parcial, case-insensitive).
    *   `climate`: Filtra planetas pelo clima (busca parcial, case-insensitive).
    *   `terrain`: Filtra planetas pelo terreno (busca parcial, case-insensitive).
*   **Paginação**: `page` (número da página, padrão: 1).

    **Exemplo**: `/planets?name=tatooine&climate=arid&page=1`

### 2. `/people`

*   **Busca por ID**: `/people/{id}`
*   **Filtros via Query Params**:
    *   `name`: Filtra personagens pelo nome (busca parcial, case-insensitive).
    *   `gender`: Filtra personagens pelo gênero (correspondência exata, case-insensitive).
    *   `film`: Filtra personagens que aparecem em um filme específico (pelo ID do filme).
*   **Paginação**: `page` (número da página, padrão: 1).

    **Exemplo**: `/people?name=luke&gender=male&film=1&page=1`

### 3. `/films`

*   **Busca por ID**: `/films/{id}`
*   **Filtros via Query Params**:
    *   `title`: Filtra filmes pelo título (busca parcial, case-insensitive).
    *   `character`: Filtra filmes que contêm um personagem específico (pelo ID do personagem).
    *   `year`: Filtra filmes pelo ano de lançamento (correspondência exata com `release_date`).
*   **Paginação**: `page` (número da página, padrão: 1).

    **Exemplo**: `/films?title=hope&character=1&year=1977&page=1`

### 4. `/starships`

*   **Busca por ID**: `/starships/{id}`
*   **Filtros via Query Params**:
    *   `name`: Filtra naves estelares pelo nome (busca parcial, case-insensitive).
    *   `model`: Filtra naves estelares pelo modelo (busca parcial, case-insensitive).
    *   `pilot`: Filtra naves estelares que foram pilotadas por um personagem específico (pelo ID do personagem).
*   **Paginação**: `page` (número da página, padrão: 1).

    **Exemplo**: `/starships?name=falcon&model=yt-1300&pilot=1&page=1`

## Testes Unitários

Testes unitários foram implementados com `pytest` para garantir a correção das funcionalidades de filtragem, paginação e transformação de dados. Para executá-los, instale `pytest` (`pip install pytest`) e execute `pytest` na raiz do projeto.

## Tecnologias Utilizadas

*   **Python 3.x**
*   **Flask**
*   **Google Cloud Functions**
*   **requests**
*   **pytest**

## Como Rodar Localmente (para desenvolvimento)

1.  Clone o repositório:
    ```bash
    git clone https://github.com/Gsn00/case-swapi.git
    cd case-swapi
    ```
2.  Crie e ative um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate   # Windows
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Para simular o ambiente do Cloud Functions localmente, execute:
    ```bash
    functions-framework --target=hello_http --debug
    ```
    A API estará disponível em `http://localhost:8080`.

## Contato

Email: silvanovaesgabriel@gmail.com
LinkedIn: https://www.linkedin.com/in/gabrielsnovais/
