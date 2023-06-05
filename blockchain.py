import hashlib
import json
from time import time
import random
import platform
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the current block is correct
            if current_block['previous_hash'] == self.hash(previous_block):
                return True

            # Check if the proof of work is valid
            if self.is_valid_proof(current_block['proof']):
                return True

        return False

    @staticmethod
    def is_valid_proof(proof):
        # Validate the proof of work
        return hashlib.sha256(str(proof).encode()).hexdigest()[:4] == '0000'
    
    def export_to_file(self, filename):
        data = {
            'chain': self.chain,
            'current_transactions': self.current_transactions
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def import_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.chain = data['chain']
            self.current_transactions = data['current_transactions']

# Example usage
blockchain = Blockchain()

login = "admin"
password = "admin"

while(1 == 1):

    print("Ctrl + C to exit")
    login_attempt = input("Login: ")
    password_attempt = input("Password: ")
        
    if(login_attempt == login and password_attempt == password):

        filename = "sample.json"

        blockchain.import_from_file(filename)

        while(1 == 1):
            print("Press 1 to add a new block")
            print("Press 2 to add a new transaction")
            print("Press 3 to see transactions")
            print("Press 4 to check if blockchain is valid")
            print("Press 5 to log out")

            x = input()

            x = int(x)

            # if(platform.system == "Windows"):
            #     os.system("cls")
            # else:
            #     os.system("clear")

            if(x == 1):
                proof = random.randint(10000, 100000)  # Placeholder for the actual proof of work
                previous_hash = blockchain.hash(blockchain.last_block)
                blockchain.create_block(proof, previous_hash)
                print("New block added!")

            elif(x == 2):
                print("The sender is: {}".format(login))

                receiver = input("Type who is the receiver: ")
                amount = input("Type the amount to transfer: ")

                blockchain.new_transaction(login, receiver, amount)

                print("Transaction complete!")

            elif(x == 3):
                for block in blockchain.chain:
                    print(json.dumps(block, indent=2))
                    print('-' * 30)

                filename = "sample.json"
                blockchain.export_to_file(filename)
                print("Blockchain exported to file:", filename)

            elif(x == 4):
                print("Is blockchain valid?", blockchain.is_valid())

            elif(x == 5):
                break

            else:
                print("Wrong key, type again")

    else: 
        print("Wrong credentials. Try again.")
        # if(platform.system == "Windows"):
        #     os.system("cls")
        # else:
        #     os.system("clear")


