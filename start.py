from google.colab import drive
drive.mount('/content/drive')

import requests
import json
import time
import csv

ETHERSCAN_API_KEY = [YOUR ETHERSCAN API KEY]
BLOCK_START =   [STRAT BLOCK]
BLOCK_END =     [END BLOCK]
CSV_FILE = '/content/drive/MyDrive/XXX.csv'

def get_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        if not json_data or 'result' not in json_data:
            print(f"Error: Empty or unexpected response: {json_data}")
            return {'result': None}

        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {'result': None}
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {'result': None}

def get_contracts_in_block(block_number, csv_writer, csvfile):
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={hex(block_number)}&boolean=true&apikey={ETHERSCAN_API_KEY}"
    block_data = get_json(url)

    if block_data['result'] is None:
        return

    if not isinstance(block_data['result'], dict) or block_data['result'].get('transactions') is None:
        print(f"Unexpected block data: {block_data['result']}")
        return

    for transaction in block_data['result']['transactions']:
        if transaction['to'] is None:
            contract_address = get_contract_address_from_receipt(transaction['hash'])
            if contract_has_withdraw_function(contract_address):
                csv_writer.writerow([contract_address])
                csvfile.flush()

def get_contract_address_from_receipt(tx_hash):
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={tx_hash}&apikey={ETHERSCAN_API_KEY}"
    receipt_data = get_json(url)

    if receipt_data['result'] is None or not isinstance(receipt_data['result'], dict):
        return None

    contract_address = receipt_data['result']['contractAddress']
    return contract_address

def contract_has_withdraw_function(contract_address):
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
    contract_abi_data = get_json(url)

    if contract_abi_data['result'] is None:
        return False

    contract_abi = contract_abi_data['result']
    if contract_abi == 'Contract source code not verified':
        return False

    try:
        contract_abi_decoded = json.loads(contract_abi)
        for entry in contract_abi_decoded:
            if entry['type'] == 'function' and entry['name'] == 'hasConfirmed':
                if check_balance(contract_address) > 0:
                    return True
    except json.JSONDecodeError as e:
        print(f"JSON decode error for contract {contract_address}: {e}")
        return False

    return False

def check_balance(contract_address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={contract_address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    balance_data = get_json(url)

    if balance_data['result'] is None:
        print(f"Could not fetch balance for contract: {contract_address}")
        return 0

    try:
        # Converting Wei to Ether
        balance = int(balance_data['result']) / (10 ** 18)
    except ValueError:
        print(f"Could not parse balance for contract: {contract_address}")
        return 0

    return balance

def main():
    with open(CSV_FILE, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Contract Address'])
        csvfile.flush()

        for block_number in range(BLOCK_START, BLOCK_END):
            print(f"Processing block {block_number}")
            get_contracts_in_block(block_number, csv_writer, csvfile)
            time.sleep(0.1)  # avoid API limit

if __name__ == "__main__":
    main()
