from classe_controle import ControleFuncionariosObras
import sqlalchemy
import os
import getpass

con = sqlalchemy.create_engine('mysql+pymysql://root:@database:3306/obras')
controle = ControleFuncionariosObras(con = con, portao = 1)

print('##### REGISTRO DE PONTOS #####')

continuar = True

while(continuar):
    cpf = input('Inserir CPF: ')
    senha = getpass.getpass()
    controle.registrar_ponto(cpf_func=cpf, senha_func=senha)
    input('Aperte Enter para continuar: ')
    os.system('clear')
    
#     input('deseja marcar')