from hashlib import sha256
from datetime import datetime
from database import ManipulateDatabase

class CreateBlockchain():
    def init(self):
        pass

    def mining_difficulty(self, hash_attempt):
        return hash_attempt.startswith('0')

    def create_genesis_block(self, time, last_hash):
        content = 'Blockchain started.'
        CreateBlockchain().create_new_block(content, time, last_hash)

    def create_new_block(self, content, time, last_hash):
        current_hash = ''
        nonce = int(time)

        while not CreateBlockchain().mining_difficulty(current_hash):
            new_block = '{}:{}:{}:{}'.format(
                content, time, last_hash, nonce)
            current_hash = sha256(new_block.encode()).hexdigest()
            nonce += 1
            
        ManipulateDatabase().record_blockchain_data(last_hash, current_hash, nonce, content)

    def new_block(self, content):
        time = datetime.utcnow().timestamp()
        last_hash = ManipulateDatabase().get_last_hash()
        
        if last_hash == 0:
            CreateBlockchain().create_genesis_block(time, last_hash)

            # PARA CONTINUAR COM OS DADOS CHAMAMOS O HASH NOVAMENTE E CRIMOS UM NOVO BLOCO
            last_hash = ManipulateDatabase().get_last_hash()
            CreateBlockchain().create_new_block(content, time, last_hash)
        else:
            CreateBlockchain().create_new_block(content, time, last_hash)