from classe_controle import ControleFuncionariosObras
import sqlalchemy
import os

con = sqlalchemy.create_engine('mysql+pymysql://sql10423050:ZGyaasVsrL@sql10.freesqldatabase.com/sql10423050')
controle = ControleFuncionariosObras(con = con, portao = 1)

print('##### REGISTRO DE PONTOS #####')

continuar = True

while(continuar):
    cpf = input('Inserir CPF: ')
    senha = input('Inserir Senha: ')
    controle.registrar_ponto(cpf_func=cpf, senha_func=senha)
    input('Aperte Enter para continuar: ')
    os.system('cls')
    
#     input('deseja marcar')