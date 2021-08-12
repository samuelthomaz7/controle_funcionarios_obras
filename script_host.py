import socket
import time
from classe_controle import ControleFuncionariosObras
import sqlalchemy


con = sqlalchemy.create_engine('mysql+pymysql://root:@database:3306/obras')


host = socket.gethostname()
port = 1024

sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #criando obj para conexão TCP com conexão IPV4

sock_obj.bind((host, port))
sock_obj.listen(5)

while True:
    clientsocket, address = sock_obj.accept()
    print(f"Connection from {address} has been established.")
    
    # time.sleep(5)
    msg = clientsocket.recv(1024)
    print(msg)
    dados_ponto = eval(msg.decode())
    controle = ControleFuncionariosObras(con = con, portao = dados_ponto['portao'])
    retorno = controle.registrar_ponto(cpf_func=dados_ponto['cpf'], senha_func=dados_ponto['senha'])
    clientsocket.send(bytes(str(retorno), 'utf-8'))
