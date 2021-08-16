## PROJETO CONTROLE DE ACESSO EM GRANDES OBRAS
Este repositório foi desenvolvido como atividade didática para a matéria Sistemas Embarcados 2021 (EESC-USP).

***
### Contextualização
**Objetivo:** Controlar o acesso de funcionários em grandes obras.

**Premissas e requisitos:**
1. Existem n portões de entrada/saída;
1. Não é possível entrar/entrar ou sair/sair;
1. Os sistemas estão conectados a um único banco de dados.
***
### Desenvolvimento

![project_diagram](https://github.com/samuelthomaz7/controle_funcionarios_obras/blob/main/wiki_images/diagrama-projeto.jpeg)

O projeto se divide em 3 grandes partes:

1. **Banco de Dados** (Docker / MySQL): 
Um container com banco de dados SQl que contém a Tabela de Funcionários, a Tabela de Obras e a Tabela de Pontos do Funcionário. Pode ser usado na nuvem ou em um servidor local. *Observação - Neste trabalho utilizamos o docker para simular um computador, pois o período de testes da ferramenta de banco de dados online FreeSQL expirou antes da conclusão do projeto.*
1. **Computador do Gestor** (Docker / Python / Pandas / SQLA):
	Um container com Python 3.8 e as bibliotecas necessárias para o programa principal de controle das obras e cadastro de funcionários. O computador do gestor tem controle sobre as tabelas do banco de dados, sendo possível visualizar e editar as obras em andamento, funcionários cadastrados, registro de ponto e portão de acesso utilizado.
1. **Sistemas Embarcados** (Python):
	Para a simulação da estrutura real proposta (uma obra com diversas entradas), containers com Python 3.8 e as bibliotecas necessárias para simular os portões (1, 2 e 3) foram criados. Para cada novo portão, um container é preciso para simular o sistema embarcado.

	Para a aplicação real, no entanto, o Docker não é necessário. Apenas o código python 'script_embarcado.py' deve ser embarcado, necessitando apenas a instalação das dependências. O script enviará via conexão TCP (como indicado no script) as informações cadastradas pelo usuário em um microcontrolador de escolha rodando python. 

	O Docker NÃO deve ser embarcado, foi utilizado apenas para simular a solução de várias placas conectadas em rede e a troca de mensagens.
***
### Informações
	
No arquivo *docker-compose.yml* temos 5 containers mapeados (banco de dados, computador do gestor e 3 portões de acesso) conectados na rede embarcados que usa o driver bridge para a conexão. Para cada portão de acesso novo, um container deve ser configurado neste arquivo, com isso respeitados o requisito número 1.

|Comando | Função|
|---|----|
| docker-compose build | configurar o docker |
| docker-compose up | rodar os containers mapeados |
| docker ps | lista os containers em execução |
| docker exec -it < NOME DO CONTAINER > bash | acessa o container escolhido |
| python filename.py | executa o arquivo python com o programa específico para o container escolhido |

| Nome do Container| Conteúdo | Arquivo Python / Comando|
|---|---|---|
| database | Parte 1 - banco de dados | mysql |
| gestor | Parte 2 - computador do gestor | gestor.py|
| ponto1 | Parte 3 - portão de acesso número 1| script_embarcado.py|
| ponto2 | Parte 3 - portão de acesso número 2| script_embarcado.py|
| ponto3 | Parte 3 - portão de acesso número 3| script_embarcado.py|
***
### Testes
Teste 1: Computador do Gestor
```
> docker exec -it gestor bash
> python gestor.py
```
1. Cadastre um funcionário
1. Confirme que o funcionário é exibido na lista da opção "1 - Verificar Funcionários"
1. Cadastre uma obra
1. Confirme que o funcionário é exibido na lista da opção "2 - Verificar Obras"

***
Teste 2: Registrar ponto
```
> docker exec -it ponto1 bash
> python registro_pontos.py
```
```
> docker exec -it ponto2 bash
> python registro_pontos.py
```
1. Registre o ponto no portão 2 com o CPF e a senha cadastrada do novo funcionário
1. Registre o ponto no portão 1 com os dados do mesmo funcionário
1. No computador do gestor, escolha a opção "3 - Verificar Pontos"
1. Confirme que o registro de entrada está relacionado com o portão 2 e o de saída com o portão 1 (Requisito número 2)

*Observação - Se o relógio do Linux não estiver sincronizado com o do Windows, o horário exibido no registro de ponto será diferente do real*

***
Teste 3: Banco de Dados
```
> docker exec -it database bash
> mysql
> use obras;
> select * from funcionarios;
```
Confirme que as informações adicionadas do novo usuário estão contidas na tabela Funcionários do banco de dados (Requisito número 3)
***
### Instruções para testes
Para melhor análise, acesse cada container em uma janela de terminal diferente.

No terminal
```
> docker-compose build
> docker-compose up
> docker ps
```
Se todos os containers configurados forem listados ao executar o último comando, podemos continuar com os testes.

***
### Teste 1: Computador do Gestor
```
> docker exec -it gestor bash
> python gestor.py
```
1. Cadastre um funcionário
1. Confirme que o funcionário é exibido na lista da opção "1 - Verificar Funcionários"
1. Cadastre uma obra
1. Confirme que o funcionário é exibido na lista da opção "2 - Verificar Obras"

***
### Teste 2: Registrar ponto
```
> docker exec -it ponto1 bash
> python script_embarcado.py
```
```
> docker exec -it ponto2 bash
> python script_embarcado.py
```
1. Registre o ponto no portão 2 com o CPF e a senha cadastrada do novo funcionário
1. Registre o ponto no portão 1 com os dados do mesmo funcionário
1. No computador do gestor, escolha a opção "3 - Verificar Pontos"
1. Confirme que o registro de entrada está relacionado com o portão 2 e o de saída com o portão 1 (Requisito número 2)

*Observação - Se o relógio do Linux não estiver sincronizado com o do Windows, o horário exibido no registro de ponto será diferente do real*

***
### Teste 3: Banco de Dados
```
> docker exec -it database bash
> mysql
> use obras
> select * from funcionarios
```
Confirme que as informações adicionadas do novo usuário estão contidas na tabela Funcionários do banco de dados (Requisito número 3)
***
