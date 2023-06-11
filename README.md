# Ethereum Smart Contract Analyzer

This project is a Python script that uses the Etherscan.io API to analyze Ethereum smart contracts within a specified block range (from `BLOCK_START` to `BLOCK_END`). It specifically looks for contracts with a `hasConfirmed` function and a non-zero Ether balance. 

The program outputs the Ethereum addresses of these contracts to a CSV file in Google Drive.

## Prerequisites

You will need to have a Google Colab account to run this code and an Etherscan API key to access the Ethereum blockchain data. Also, Google Drive is used for storing the output file.

## Usage

1. Replace `ETHERSCAN_API_KEY` with your actual Etherscan API key.
2. Set the `BLOCK_START` and `BLOCK_END` to the range of Ethereum blocks you want to analyze.
3. Set the `CSV_FILE` to the path where you want the CSV file to be stored in your Google Drive. Make sure you have the necessary write permissions to this location.
4. Run the script. It will mount your Google Drive and start analyzing the Ethereum blocks. For each smart contract with a `hasConfirmed` function and a non-zero Ether balance, it will write the Ethereum address of the contract to the CSV file.

## How it Works

1. The script iterates over every Ethereum block in the given range.
2. For each block, it retrieves all transactions in the block.
3. If the transaction's `to` field is `None`, it indicates a contract creation transaction. The script then fetches the contract address from the transaction receipt.
4. It checks the contract ABI to see if it has a `hasConfirmed` function.
5. If the contract has a `hasConfirmed` function, it then checks if the contract's balance is greater than zero.
6. If the contract's balance is greater than zero, it writes the contract address to the CSV file.

## Note

The script includes a delay (`time.sleep(0.1)`) between requests to avoid hitting Etherscan API rate limits. Depending on the size of your block range, the script could take a while to complete.

## Disclaimer

This project is intended for educational purposes only. Always respect the Etherscan API terms of service and be aware that querying extensive block ranges could lead to rate limiting or banning. Always handle blockchain data responsibly.
