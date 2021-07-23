from classe_controle import ControleFuncionariosObras
import sqlalchemy
import os

con = sqlalchemy.create_engine('mysql+pymysql://root:@database:3306/obras')
print(con)
controle = ControleFuncionariosObras(con = con, portao = 1)

continuar = True

while(continuar):

    print('''

    ##### ESCOLHA A OPÇÃO #####

    1 - Verificar Funcionários
    2 - Verificar Obras
    3 - Verificar Pontos
    4 - Cadastrar Obra
    5 - Cadastrar Funcionário
    6 - Sair

    ''')
    print()
    escolha = int(input('digite :'))


    if(escolha == 1):
        print(controle.ler_dados_sql_funcionarios())
    elif(escolha == 2):
        print(controle.ler_dados_sql_obras())
    elif(escolha == 3):
        print(controle.ler_dados_sql_pontos())
    elif(escolha == 4):
        print(controle.cadastrar_obra(tabela_nova=False))
    elif(escolha == 5):
        controle.cadastrar_funcionario(tabela_nova=True)
    elif(escolha == 6):
        continuar = False
        
    input('Aperte Enter para continuar: ')
    os.system('clear')
    