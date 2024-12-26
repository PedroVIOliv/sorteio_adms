# Sorteio de ADMs por Altura de Bloco

Este projeto é uma aplicação web que realiza um sorteio mensal de administradores de um grupo, utilizando a altura de blocos da blockchain como base para determinar o momento do sorteio e o hash do bloco como semente para selecionar os novos administradores.

## Funcionalidades

- Obtém a altura atual de blocos da blockchain via API do Blockstream.
- Utiliza o hash do bloco alvo como semente para um sorteio determinístico.
- Animação para destacar os vencedores na interface web.
- Atualização em tempo real do status do sorteio via polling.
- Página web interativa com informações sobre o sorteio.

## Requisitos

- Python 3.8 ou superior
- Flask
- Requests
- Dotenv

## Configuração

1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto para configurar o bloco alvo:

```bash
TARGET_BLOCK_HEIGHT=700000
```

Se o bloco alvo não for definido, o valor padrão será `700000`.

4. Execute o servidor Flask:

```bash
python app.py
```

5. Acesse a aplicação em seu navegador:

```bash
http://localhost:5000
```

## Estrutura do Projeto

- **app.py**: Arquivo principal que contém a lógica do servidor Flask.
- **templates/index.html**: Página HTML renderizada pelo Flask.
- **static/style.css**: Arquivo de estilos para a interface web.
- **.env**: Arquivo de configuração contendo variáveis de ambiente.
- **requirements.txt**: Lista de dependências do Python.

## Como Funciona o Sorteio

1. O programa verifica constantemente a altura atual da blockchain via API.
2. Quando a altura do bloco alvo é atingida, o hash do bloco é utilizado como semente para selecionar aleatoriamente dois membros elegíveis como novos administradores.
3. A interface web exibe os membros eliminados e destaca os vencedores com uma animação.