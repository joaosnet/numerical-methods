# Métodos Numéricos

![Tamanho do repositório do GitHub](https://img.shields.io/github/repo-size/joaosnet/numerical-methods?style=for-the-badge)
![Contagem de linguagens do GitHub](https://img.shields.io/github/languages/count/joaosnet/numerical-methods?style=for-the-badge)
![Forks do GitHub](https://img.shields.io/github/forks/joaosnet/numerical-methods?style=for-the-badge)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg?style=for-the-badge)](https://github.com/joaosnet/numerical-methods/blob/master/README.pt-br.md)

<img align="right" src="screenshots/dash.png" width="256"/>

## Introdução

O projeto **Métodos Numéricos** oferece uma plataforma interativa para explorar métodos numéricos aplicados à engenharia. Desenvolvido em Python, o aplicativo permite a aplicação e visualização de algoritmos matemáticos, sendo útil para aprendizado e análises. O site está disponível [aqui](https://numerical-methods-7wxf.onrender.com/).

## Tecnologias Utilizadas

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" /> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" /> <img src="https://img.shields.io/badge/dash-008DE4?style=for-the-badge&logo=dash&logoColor=white" /> <img src="https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D" />

## Índice

* [Introdução](#introdução)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Como Usar](#como-usar)
* [Capturas de Tela](#capturas-de-tela)
* [Contribuindo](#contribuindo)
* [Atualizando o Repositório](#atualizando-o-repositório)

## Como Usar

### Pré-requisitos

1. Instale o gerenciador `pyenv` para gerenciar versões do Python:
   - [Instruções para Windows](https://github.com/pyenv-win/pyenv-win#installation)
   - [Instruções para Linux](https://github.com/pyenv/pyenv#installation)
   
2. Instale o `pipx` para gerenciar dependências isoladas.

### Instalação

#### Windows e Linux

1. Atualize o `pyenv`:
   ```bash
   pyenv update
   ```
2. Instale o Python 3.12:
   ```bash
   pyenv install 3.12
   ```
3. Defina o ambiente Python local e global:
   ```bash
   pyenv local 3.12
   pyenv global 3.12
   ```
4. Instale o `pipx`:
   ```bash
   pip install pipx
   ```
5. Instale o `poetry` com o `pipx`:
   ```bash
   pipx install poetry
   ```
6. Configure o `poetry` para criar o ambiente virtual no diretório do projeto:
   ```bash
   poetry config virtualenvs.in-project true
   ```
7. Clone o repositório:
   ```bash
   git clone https://github.com/joaosnet/numerical-methods.git
   ```
8. Instale as dependências do projeto:
   ```bash
   poetry install
   ```
9. Execute o aplicativo:
   ```bash
   python main.py
   ```
   
### Criar o arquivo `requirements.txt`

Caso precise de um arquivo `requirements.txt` para outras implementações:

```bash
poetry export --without-hashes --without-urls --without dev -f requirements.txt -o requirements.txt
```

## Capturas de Tela

![Captura de Tela](screenshots/dash.png)

_Visualização do dashboard mostrando métodos numéricos aplicados._

## Contribuindo

Se deseja contribuir para o desenvolvimento do projeto, siga os passos abaixo:

1. Faça um fork do repositório.
2. Clone seu fork para o ambiente local.
3. Crie uma nova branch para suas alterações:
   ```bash
   git checkout -b nome-da-sua-branch
   ```
4. Realize as modificações e faça commit:
   ```bash
   git commit -m "Descrição das alterações"
   ```
5. Envie suas mudanças para o repositório remoto:
   ```bash
   git push origin nome-da-sua-branch
   ```
6. Abra um pull request no repositório original.

## Atualizando o Repositório

Para manter o repositório atualizado com as últimas mudanças:

1. Puxe as últimas mudanças:
   ```bash
   git pull
   ```
2. Adicione novos arquivos ou alterações:
   ```bash
   git add .
   ```
3. Faça commit das mudanças:
   ```bash
   git commit -m "Atualizando repositório"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push
   ```
