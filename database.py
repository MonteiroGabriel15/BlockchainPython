import pyodbc

class ManipulateDatabase():
    def __init__(self):
        # DADOS DE LOCALIZAÇÃO DA BLOCKCHAIN NO BANCO
        self.database_driver = "SQL Server"
        self.server = "DESKTOP-HGT2ISC"
        self.database = "Blockchain"
        self.user = ""
        self.password = ""
        self.port = 1433
        self.version = 9.0
        self.mutable = "Blocks"

    def connect_immutable_database(self):

        # FAZ CONEXÃO COM O BANCO QUE OS ARQUIVOS SERÃO ESCRITOS
        try:
            connection = pyodbc.connect(
                f"""DRIVER={self.database_driver};SERVER={self.server};PORT={self.port};DATABASE={self.database};UID={self.user};PWD={self.password};TDS_Version={self.version};')""")
        except Exception as error:
            con = f"""BLOCKCHAIN CONNECTION ERROR
            {error}"""
            exit()

        else:
            con = "BLOCKCHAIN CONNECTION SUCCESS"
            return connection

        finally:
            print(con)

    def get_last_hash(self):

        # FAZ PEDIDO DE CONEXÃO
        cursor = ManipulateDatabase().connect_immutable_database().cursor()
        # FAZ A SEARCH NO Banco DE FORMA QUE O ULTIMO ID SEJA SELECIONADO 1°
        search = f"""SELECT TOP 1 [CURRENT_HASH] FROM [dbo].[{self.mutable}] ORDER BY ID DESC"""
        cursor.execute(search)
        retorno = cursor.fetchone()
        last_hash = retorno[0]
        
        return last_hash

    def record_blockchain_data(self,last_hash, current_hash, nonce, content):

        # FAZ PEDIDO DE CONEXÃO
        cursor = ManipulateDatabase().connect_immutable_database().cursor()

        # INSERE O BLOCO NA TABELA MUTÁVEL
        insert = f"""INSERT INTO {self.mutable}(LAST_HASH,CURRENT_HASH,NOCNE,CONTENT)
                VALUES('{last_hash}','{current_hash}','{nonce}','{content}');"""
        cursor.execute(insert)

        # INSERT OS DADOS NA BLOCKCAHIN
        cursor.commit()
        cursor.close()

        # DELETA OS DADOS DA TABELA MUTÁVEL PARA QUE ELA VÁ PARA A TABELA IMUTÁVEL
        # delete = f"""DELETE FROM [dbo].[{self.mutable}]"""
        # cursor.execute(delete)
        # cursor.commit()
        # cursor.close()


