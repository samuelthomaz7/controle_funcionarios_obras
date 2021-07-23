from classe_controle import ControleFuncionariosObras
import sqlalchemy
import os
import getpass

#cria a conexão com o SQL
con = sqlalchemy.create_engine('mysql+pymysql://root:@database:3306/obras')
#le a variável de ambiente relativa ao portao em que roda o controle de pontos
portao = int(os.environ['ponto'])
#instancia a classe
controle = ControleFuncionariosObras(con = con, portao = portao)

print(f'##### REGISTRO DE PONTOS PORTÃO {portao} #####')

continuar = True

#recebe as informações do funcionário para cadastro de ponto
while(continuar):
    cpf = input('Inserir CPF: ')
    senha = getpass.getpass()
    controle.registrar_ponto(cpf_func=cpf, senha_func=senha)
    input('Aperte Enter para continuar: ')
    os.system('clear')
    
