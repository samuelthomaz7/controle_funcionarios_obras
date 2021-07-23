from classe_controle import ControleFuncionariosObras
import sqlalchemy
import os
import getpass

con = sqlalchemy.create_engine('mysql+pymysql://root:@database:3306/obras')
portao = int(os.environ['ponto'])
controle = ControleFuncionariosObras(con = con, portao = portao)

print(f'##### REGISTRO DE PONTOS PORTÃO {portao} #####')

continuar = True

while(continuar):
    cpf = input('Inserir CPF: ')
    senha = getpass.getpass()
    controle.registrar_ponto(cpf_func=cpf, senha_func=senha)
    input('Aperte Enter para continuar: ')
    os.system('clear')
    
