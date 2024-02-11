from bit import Key
from multiprocessing import cpu_count
from time import sleep, time

def generate_random_address():
        key = Key()
        print("\n Public Address: "+key.address)
        print(" Private Key: "+key.to_wif())
    
def generate_address_fromKey(privateKey):
    if privateKey != "":
        key = Key(privateKey)
        print("\n Public Address: "+key.address)
        print("\n Your wallet is ready!")
    else:
        print("no entry")

def num_of_cores() -> int:
        available_cores = cpu_count()
        cores = input(f"\nNumber of available cores: {available_cores}\n \n How many cores to be used? (leave empty to use all available cores) \n \n Type something>")
        if cores.isdigit():
            cores = int(cores)
            if 0 < cores <= available_cores:
                return cores
        raise ValueError("Too dumb to enter an amount of cores!")

def random_brute(loaded_addresses, i, start_time):
    key = Key()
    if key.address in loaded_addresses:
            print("Wow matching address found!!")
            print("Public Adress: "+key.address)
            print("Private Key: "+key.to_wif())
            f = open("foundkey.txt", "a") # the found privatekey and address saved to "foundkey.txt"
            f.write(key.address+"\n")
            f.write(key.to_wif()+"\n")
            f.close()
            sleep(510)
            exit()
    if i != 0 and i % 10_000_000 == 0:
        print(f"i: {i} | {(time()-start_time)/3600:.2f}h")
        print(f"Current address {key.address} and current key {key.to_wif()}")
          