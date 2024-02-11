import requests
from bit import Key
from time import sleep, time
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
import gzip
import random
import sys
import BalanceDownload
import Utils


balance_file_name = "le_addresses.gz"
download_latest_balances_url = "http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz"

            
def get_user_input(argv):
    user_input = input("\n What do you want to do? \n \n   [1]: generate random key pair \n   [2]: generate public address from private key \n   [3]: brute force bitcoin offline mode \n   [0]: exit \n \n Type something>")
    if user_input == "1":
        Utils.generate_random_address()
        print("\n Your wallet is ready!")
        input("\n Press Enter to exit")
        exit()
    elif user_input == "2":
        privateKey = input("\n Enter Private Key>")
        try:
            Utils.generate_address_fromKey(privateKey)
        except:
            print("\n incorrect key format")
        input("Press Enter to exit")
        exit()
    elif user_input == "3":
        method_input = input(" \n Enter the desired number: \n \n   [1]: random attack \n   [0]: exit \n \n Type something>")
        if method_input=="1":
            if hasToDownload(argv):
                BalanceDownload.download_latest_balance_txt(download_latest_balances_url, balance_file_name)
            loaded_addresses = BalanceDownload.prepare_loaded_addresses(balance_file_name)
            target = Utils.random_brute
        else:
            print("exitting...")
            exit()
    elif user_input == "0":
        print("exitting")
        sleep(2)
        exit()
    with ThreadPoolExecutor(max_workers=Utils.num_of_cores()) as pool:
        start_time = time()
        print("\n Starting ...", start_time)
        i=0
        while True:
            if i != 0 and i % 10_000_000 == 0:
                print(f"i: {i} | {(time()-start_time)/3600:.4f}h")
                BalanceDownload.download_latest_balance_txt(download_latest_balances_url, balance_file_name)
                loaded_addresses = BalanceDownload.prepare_loaded_addresses(balance_file_name)

            if pool._work_queue.qsize() > 10000:
                sleep(1)
            else:
                pool.submit(target, loaded_addresses, i, start_time)
                i = i+1
        print("Stopping\n")
        exit()

def hasToDownload(argv):
    return len(argv) > 1 and (argv[1].lower() == '-d' or argv[1].lower() == "--download")

if __name__ == "__main__":
    get_user_input(sys.argv)
            
    
