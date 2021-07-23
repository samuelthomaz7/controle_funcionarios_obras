import pandas as pd
import datetime
import sqlalchemy
import getpass

class ControleFuncionariosObras():
    
    def __init__(self, con, portao):
        self.con = con
        self.portao = portao
        
    
    def ler_dados_sql_funcionarios(self):
        
        funcionarios = pd.read_sql(sql = 'funcionarios', con=self.con)
        return funcionarios.drop('senha', axis = 1)
    
    def ler_dados_sql_obras(self):
        
        obras = pd.read_sql(sql = 'obras', con=self.con)
        return obras
    
    def ler_dados_sql_pontos(self):
        
        pontos = pd.read_sql(sql = 'registro_pontos', con=self.con)
        return pontos
    
    def cadastrar_funcionario(self, dados_funcionario = None, tabela_nova = True):
        
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
            df_func.to_sql(name = 'funcionarios', con = self.con, if_exists='append', index = False)
            
        else:
        
            funcionarios = self.ler_dados_sql_funcionarios()
            
            if(dados['cpf'] in funcionarios.cpf.to_list()):
                print('funcionario já cadastrado anteriormente, favor inserir outro')
                
            else:
                dados['senha'] = self.cadastro_senha()
                df_func = pd.DataFrame(dados, index = [0])
                df_func = pd.concat([funcionarios, df_func ], axis = 0)
                df_func.to_sql(name = 'funcionarios', con = self.con, if_exists='replace', index = False)
            
    
        
    
    def registrar_ponto(self, cpf_func, senha_func):
        
        funcionarios = self.ler_dados_sql_funcionarios()
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

