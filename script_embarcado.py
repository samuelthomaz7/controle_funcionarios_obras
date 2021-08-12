from classe_controle import ControleFuncionariosObras
import os
import getpass
import socket


#cria a conexão com o SQL
# con = sqlalchemy.create_engine('mysql+pymysql://root:@database:3306/obras')
#le a variável de ambiente relativa ao portao em que roda o controle de pontos
portao = int(os.environ['ponto'])
#instancia a classe
# controle = ControleFuncionariosObras(con = con, portao = portao)

host = '172.21.0.6'
port = 1024

print(f'##### REGISTRO DE PONTOS PORTÃO {portao} #####')

continuar = True

#recebe as informações do funcionário para cadastro de ponto
while(continuar):
    cpf = input('Inserir CPF: ')
    senha = getpass.getpass()

    sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #criando obj para conexão TCP com conexão IPV4
    sock_obj.connect((host, port))

    # msg = sock_obj.recv(1024)
    # print(msg.decode("utf-8"))
    # controle.registrar_ponto(cpf_func=cpf, senha_func=senha)
    string_ponto = str({
        'cpf': cpf,
        'senha': senha,
        'portao': portao
    })

    sock_obj.sendto(bytes(string_ponto, 'utf-8'), (host, port))
    retorno = int(sock_obj.recv(1024).decode())

    print('\n\n')

    if(retorno == 0):
        print('Ponto registrado com sucesso!')
    elif(retorno == 1):
        print('Senha Incorreta! Tentar novamente')
    else:
        print('Funcionário não cadastrado')

    print('\n')

    input('Aperte Enter para continuar: ')

    
    os.system('clear')
    
