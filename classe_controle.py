import pandas as pd
import datetime
import sqlalchemy
import getpass

class ControleFuncionariosObras():

    '''
    Classe que tem como objetivo centralizar todas as funções e atributos do programa de Controle de Funcionários em obras

    Input:
        - con -> engine do tipo sqlalchemy para conectarmos a um banco de dados no qual escreveremos as informações
        - portao -> informar o número do portão em que o programa será executado
    
    
    '''
    
    def __init__(self, con, portao=None):
        self.con = con
        self.portao = portao
        
    
    def ler_dados_sql_funcionarios(self, mostrar_senha = False):

        '''
        Função que tem como objetivo ler os dados de funcionários do SQL e trazer para o python

        Input:
            - mostrar_senha -> bool se devemos ou nao mostrar a senha dos funcionários
        Output:
            - funcionarios -> tabela com as informações dos funcionários
        
        '''
        
        funcionarios = pd.read_sql(sql = 'funcionarios', con=self.con)
        if(mostrar_senha):
            return funcionarios
        else:
            return funcionarios.drop('senha', axis = 1)


        
    
    def ler_dados_sql_obras(self):

        '''
        Função que tem como objetivo ler os dados de obras do SQL e trazer para o python

        Input:
            - 
        Output:
            - obras -> tabela com as informações dos funcionários
        
        '''
        
        obras = pd.read_sql(sql = 'obras', con=self.con)
        return obras
    
    def ler_dados_sql_pontos(self):

        '''
        Função que tem como objetivo ler os dados de registro de pontos do SQL e trazer para o python

        Input:
            - 
        Output:
            - obras -> tabela com as informações dos funcionários
        
        '''
        
        pontos = pd.read_sql(sql = 'registro_pontos', con=self.con)
        return pontos
    
    def cadastrar_funcionario(self, dados_funcionario = None, tabela_nova = True):

        '''
        Função que tem como objetivo cadastrar novos funcionários e registrá-los no SQL

        Input:
            - dados_funcionario -> argumento utilizado durante o desenvolvimento que recebe um dicionário com as informações do funcionário
            - tabela_nova -> caso a tabela não exista no SQL ainda, setamos esta variável como True para criar uma nova
        Output:
            - 
        
        '''
        
        if(dados_funcionario != None):
            dados = dados_funcionario.copy() 
        else:
            dados = {}
            for atributo in ['nome', 'data_nascimento', 'cpf', 'cargo', 'inicio_jornada', 'fim_jornada', 'id_obra']:
                if(atributo == 'data_nascimento'):
                    dados[atributo] = pd.to_datetime(input(f'inserir {atributo}: '), dayfirst=True)
                else:                    
                    dados[atributo] = input(f'inserir {atributo}: ')
        
        if(tabela_nova):
            dados['senha'] = self.cadastro_senha()
            df_func = pd.DataFrame(dados, index = [0])
            df_func.to_sql(name = 'funcionarios', con = self.con, if_exists='replace', index = False)
            
        else:
        
            funcionarios = self.ler_dados_sql_funcionarios(mostrar_senha=True)
            
            if(dados['cpf'] in funcionarios.cpf.to_list()):
                print('funcionario já cadastrado anteriormente, favor inserir outro')
                
            else:
                dados['senha'] = self.cadastro_senha()
                df_func = pd.DataFrame(dados, index = [0])
                df_func = pd.concat([funcionarios, df_func ], axis = 0)
                df_func.to_sql(name = 'funcionarios', con = self.con, if_exists='replace', index = False)
            
    
        
    
    def registrar_ponto(self, cpf_func, senha_func):


        '''
        Função que tem como objetivo registrar o ponto de um funcionário e guardar a informação de entrada no SQL

        Input:
            - cpf_func -> CPF do funcionário
            - senha_func -> senha do funcionário
        Output:
            - 
        
        '''
        
        funcionarios = self.ler_dados_sql_funcionarios(mostrar_senha = True)
        pontos = self.ler_dados_sql_pontos()
        
        if(cpf_func in funcionarios.cpf.to_list()):
            funcionario = funcionarios.query(f"cpf == '{cpf_func}'").copy()
            
            senha = funcionario.senha.iloc[0]
            
            if(senha != senha_func):
                print('senha incorreta!')
            else:
                pontos_funcionario = pontos.query(f"cpf == '{cpf_func}'")
                
                if(pontos_funcionario.shape[0] == 0):
                    
                    df_ponto = pd.DataFrame({
                                    'cpf': cpf_func,
                                    'horario': datetime.datetime.today(),
                                    'portao': self.portao,
                                    'tipo': 'entrada'
                                }, index = [0])

                    df_ponto.to_sql('registro_pontos', con = self.con, if_exists='append', index = False)
                    
                else:
                
                    tipo_ultima_entrada = pontos_funcionario.sort_values(by='horario' ,ascending = False).tipo.iloc[0]
                    if(tipo_ultima_entrada == 'entrada'):
                        tipo = 'saida'
                    else:
                        tipo = 'entrada'

                    df_ponto = pd.DataFrame({
                                    'cpf': cpf_func,
                                    'horario': datetime.datetime.today(),
                                    'portao': self.portao,
                                    'tipo': tipo
                                }, index = [0])

                    df_ponto.to_sql('registro_pontos', con = self.con, if_exists='append', index = False)
                    print('ponto cadastrado com sucesso !')

                
                return df_ponto
                
            
        else:
            print('funcionario nao cadastrado!')
        
    def cadastrar_obra(self, dados_obra = None, tabela_nova = True):


        '''
        Função que tem como objetivo cadastrar novas obras e registrá-las no SQL

        Input:
            - dados_obra -> argumento utilizado durante o desenvolvimento que recebe um dicionário com as informações da obra
            - tabela_nova -> caso a tabela não exista no SQL ainda, setamos esta variável como True para criar uma nova
        Output:
            - 
        
        '''
        

        if(dados_obra != None):
            dados = dados_obra.copy()
            
            
        else:
            dados = {}
            for atributo in ['nome', 'cidade', 'UF', 'contratante', 'numero', 'cep', 'inicio', 'fim']:
                dados[atributo] = input(f'inserir {atributo}: ')
        
        

        if(tabela_nova):
            dados['id_obra'] = 1
            df_obra = pd.DataFrame(dados, index = [0])
            df_obra.to_sql(name = 'obras', con = self.con, if_exists='append', index = False)
        else:
        
            obras = self.ler_dados_sql_obras()
            if((dados['numero'] in obras.numero.to_list()) and (dados['cep'] in obras.cep.to_list()) and (dados['nome'] in obras.nome.to_list())):
                print('obra já cadastrada anteriormente, por favor inserir outra')
                
            else:
                if(('id_obra' not in obras.columns) or (obras.shape[0] == 0)):
                    dados['id_obra'] = 1
                    
                else:
                    id_ultima_obra = obras.sort_values(by = 'id_obra', ascending = False).id_obra.iloc[0]
                    dados['id_obra'] = id_ultima_obra + 1
                    
                    
                df_obra = pd.DataFrame(dados, index = [0])
                df_obra.to_sql(name = 'obras', con = self.con, if_exists='append', index = False)

        return dados
    
    def cadastro_senha(self):

        '''
        Função que tem como objetivo receber a senha do usuário sem aparecer na tela

        Input:
            - 
        Output:
            - senha -> string com a senha cadastrada
        
        '''
        senha = 0
        conf_senha = 1
        while (senha != conf_senha):
            senha = getpass.getpass()
            conf_senha = getpass.getpass()
        
        return senha
    
#     def get_funcionarios(self):
#         return pd.read_sql(sql = 'funcionarios', con=conn)
    
#     def get_obras(self):
#         return pd.read_sql(sql = 'obras', con=conn)
    
#     def get_pontos(self):
#         return pd.read_sql(sql = 'registro_pontos', con=conn)

