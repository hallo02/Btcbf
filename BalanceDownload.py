import requests
import sys
import gzip
import random

balance_check_url = "https://blockchain.info/q/addressbalance/"

def prepare_loaded_addresses(balance_file_name):
    print("Start loading addresses into memory")
    with gzip.open(balance_file_name, "rt") as f:
        loaded_addresses = f.readlines()
    loaded_addresses = [x.rstrip() for x in loaded_addresses]
    # Remove invalid wallet addresses
    loaded_addresses = [x for x in loaded_addresses if x.find('wallet') == -1 and len(x) > 0]
    random_selection = random.sample(loaded_addresses,2)
    checkRandomAddresses(random_selection)
    print("Successfully loaded", len(loaded_addresses), "addresses into memory")
    return set(loaded_addresses)
     

def download_latest_balance_txt(download_latest_balances_url, balance_file_name):
        print("Start downloading", download_latest_balances_url)
        response = requests.get(download_latest_balances_url, stream=True)
        total = int(response.headers.get('content-length', 0))
        with open(balance_file_name, mode="wb") as file:
            loaded = 0
            for chunk in response.iter_content(chunk_size=10 * 1024):
                loaded += len(chunk)
                progress = 100 / total * loaded
                sys.stdout.write("Download progress: %d%%   \r" % (progress) )
                sys.stdout.flush()
                file.write(chunk)
        print("Download completed")

def checkRandomAddresses(selection):
    print("--------------------------------------------")
    print("Init some balance checks of loaded addresses")
    for address in selection:
        url = balance_check_url + address
        balance = int(requests.get(url).text) / 100_000_000
        print(address, "has", balance, "bitcoins")
    print("--------------------------------------------")