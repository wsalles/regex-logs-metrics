# Challenge Accepted (GLOG-API)

Aplicação desenvolvida para processar arquivos de log e criar métricas para tomada de decisão.

## Começando o Desafio

Nosso principal produto possui um webserver(nginx) que recebe milhões de requests por dia. 

Esse desafio consiste em construir uma API que receberá um arquivo de log gerado em um desses webservers, efetue um processamento, e retorne informações e estatísticas sobre o mesmo, para que possamos detectar padrões, anomalias e possíveis problemas. Enviamos em anexo um log de exemplo.

O log possui o seguinte formato (sem quebras de linha):
```bash
'$remote_addr - $remote_user [$time_local] $host "$request" '
'$status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for" '
'request_time[$request_time] Proxy_subrequest[$proxy_host$uri$is_args$args] '
'Proxy: $upstream_cache_status $upstream_status $upstream_response_time '
'Cache-Control: $upstream_http_cache_control '
'Expires: $upstream_http_expires '
'Scheme: $scheme '
'SSL: $http2 $ssl_server_name $ssl_session_id $ssl_session_reused $ssl_protocol $ssl_cipher'
```

## Pré-requisitos

Foi escolhida a linguagem de programação [Python 3](https://www.python.org/) para realizar essa tarefa.

Utilizamos o gerenciador de pacote [pip](https://pip.pypa.io/en/stable/) para realizar a instalação das dependências do projeto:

```bash
pip install -r requirements.txt
```
requirements.txt:
```
aniso8601==4.1.0
Click==7.0
Flask==1.0.2
Flask-RESTful==0.3.7
itsdangerous==1.1.0
Jinja2==2.10
MarkupSafe==1.1.1
pytz==2018.9
six==1.12.0
Werkzeug==0.14.1
```

## Criação do ambiente local
#### 1) Instalar o Python 3 (CentOS/RedHat)

```
yum install python3 python3-pip
```

#### 2) Realizar o pull do projeto:
```shell
git clone https://wsalles@bitbucket.org/wsalles/challenge_accepted.git
```

#### 3) Criar o ambiente virtual (VirtualEnv)

```
python3 -m venv venv
```
#### 4) Iniciar o ambiente virtual:

```
./venv/bin/activate
```

#### 5) Executar a aplicação:
```
python challenge_accepted/app.py
```

## Bitbucket + Heroku CI/CD

### 1) Criando contas:
#### 1.1) BitBucket:
```shell
https://bitbucket.org/account/signup/
```
#### 1.2) Heroku:
```shell
https://id.heroku.com/login
```

### 2) Configurações:
#### 2.1) Crie sua pipeline no Heroku e em seguida crie seu app:
```
https://dashboard.heroku.com/apps
```

#### 2.2) Capture a chave da API do Heroku, em:
```
Dashboard > Profile > Accounts Settings > API Key e clique em Reveal
```

#### 2.3) Crie seu próprio repositório no Bitbucket e suba o projeto:
```
https://bitbucket.org/repo/create
```
#### 2.4) Ainda no BitBucket, configure o seu repositório em:
```
Settings > PIPELINES > Deployments

HEROKU_APP_NAME=<nome_da_aplicacao_criada_no_heroku(vide item 2.1)>
HEROKU_API_KEY=<chave_autorizadora(vide item 2.2)>
```

#### 2.5) Para criar a pipeline no BitBucket, é necessário ter o arquivo 'bitbucket-pipelines.yml' na raiz do seu projeto com as seguintes configurações:
```
image: python:latest

clone:
  depth: full
  
pipelines:
  branches:
    master:
      - step:
          caches:
            - pip
          script:
            - pip install -r requirements.txt
      - step:
                name: Deploy to Heroku
                deployment: staging #production
                script:
                  - git push https://heroku:$HEROKU_API_KEY@git.heroku.com/$HEROKU_APP_NAME.git HEAD
```


### 3) Build + Deploy
Essa é o grande momento onde todos os nossos feitos se tornam realidade.

#### 3.1) Build
###### Se todas as configurações acima estiverem corretas, basta realizar um commit e um push para a branch master para acionar a trigger do pipeline no Bitbucket.

###### 3.1.1) Irá realizar o build da imagem python (última versão);
###### 3.1.2) Realiza a copia de todo repositório para dentro da imagem;
###### 3.1.3) Executa a instalação das dependências do python

#### 3.2) Deploy
###### O último step da pipeline do BitBucket é o Deploy no Heroku.
###### Basta acessar o site do Heroku e clicar em Open App:
```
Personal > Sua Pipeline > Seu App > Open App
```

## Créditos:
[https://regex101.com/](https://regex101.com/)

[https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml)

[https://confluence.atlassian.com/bitbucket/deploy-to-heroku-872013667.html](https://confluence.atlassian.com/bitbucket/deploy-to-heroku-872013667.html)

## Mais informações:
[Documentação e Apresentação](https://bitbucket.org/wsalles/challenge_accepted/src/master/docs.pptx)

## Autor
Wallace Salles <[wallace_robinson@hotmail.com](wallace_robinson@hotmail.com)>