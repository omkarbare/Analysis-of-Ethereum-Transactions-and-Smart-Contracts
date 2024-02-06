# Ethereum Analysis using Hadoop MapReduce

Provided here is the analysis of Ethereum transactions and smart contracts which have occurred on the Ethereum network using series of Map/Reduce jobs. Source codes of how this analysis was carried out is also provided.

Initially released in 2015, Ethereum is a blockchain-based distributed computing platform. It allows users to exchange currency being Ether, buy or sell their services using smart contracts, along with many other applications.

## The Dataset

Tools allow scraping of all block/transactions and they are dumped into CSV files to be processed in bulk (notably [Ethereum-ETL](https://github.com/blockchain-etl/ethereum-etl)). These dumps are uploaded daily into a repository on Google [BigQuery](https://bigquery.cloud.google.com/dataset/bigquery-public-data:crypto_ethereum?pli=1) which is the source of the dataset for the analysis undertaken here. A subset of the data was uploaded to HDFS to enable the execution of the Map/Reduce jobs. The blocks, contracts and transactions tables have been pulled down and been stripped of unneeded fields to reduce their size. Also used was a set of scams which can be either active and inactive, run on the Ethereum network via [etherscamDB](https://etherscamdb.info/scams) which is was uploaded to HDFS.

### Dataset - Blocks CSV File

| Column Name           | Decription                                                   | Example              |
| --------------------- | ------------------------------------------------------------ | -------------------- |
| **number**            | The block number                                             | 4776199              |
| **hash**              | Hash of the block                                            | 0x9172600443ac88e... |
| **miner**             | The address of the beneficiary to whom the mining rewards were given | 0x5a0b54d5dc17e0a... |
| **difficulty**        | Integer of the difficulty for this block                     | 1765656009004680     |
| **size**              | The size of this block in bytes                              | 9773                 |
| **gas_limit**         | The maximum gas allowed in this block                        | 7995996              |
| **gas_used**          | The total used gas by all transactions in this block         | 2042230              |
| **timestamp**         | The timestamp for when the block was collated                | 1513937536           |
| **transaction_count** | The number of transactions in the block                      | 62                   |

### Dataset - Transactions CSV File

| Column Name         | Decription                                                   | Example              |
| ------------------- | ------------------------------------------------------------ | -------------------- |
| **block_number**    | Block number where this transaction was in                   | 6638809              |
| **from_address**    | Address of the sender                                        | 0x0b6081d38878616... |
| **to_address**      | Address of the receiver. null when it is a contract creation transaction | 0x412270b1f0f3884... |
| **value**           | Value transferred in Wei (the smallest denomination of ether) | 240648550000000000   |
| **gas**             | Gas provided by the sender                                   | 21000                |
| **gas_price**       | Gas price provided by the sender in Wei                      | 5000000000           |
| **block_timestamp** | Timestamp the associated block was registered at (effectively timestamp of the transaction) | 1541290680           |

### Dataset - Contracts CSV File

| Column Name         | Decription                                                   | Example              |
| ------------------- | ------------------------------------------------------------ | -------------------- |
| **address**         | Address of the contract                                      | 0x9a78bba29a2633b... |
| **is_erc20**        | Whether this contract is an ERC20 contract                   | false                |
| **is_erc721**       | Whether this contract is an ERC721 contract                  | false                |
| **block_number**    | Block number where this contract was created                 | 8623545              |
| **block_timestamp** | Timestamp the associated block was registered at (effectively timestamp of the transaction) | 2019-09-26 08:50:... |

### Dataset - Scams JSON File

| Category Name   | Decription                                                   | Example                     |
| --------------- | ------------------------------------------------------------ | --------------------------- |
| **id**          | Unique ID for the reported scam                              | 81                          |
| **name**        | Name of the Scam                                             | "myetherwallet.us"          |
| **url**         | Hosting URL                                                  | "http://myetherwallet.us"   |
| **coin**        | Currency the scam is attempting to gain                      | "ETH"                       |
| **category**    | Category of scam - Phishing, Ransomware, Trust Trade, etc.   | "Phishing"                  |
| **subcategory** | Subdivisions of Category                                     | "MyEtherWallet"             |
| **description** | Description of the scam provided by the reporter and datasource | "did not 404.,MEW Deployed" |
| **addresses**   | List of known addresses associated with the scam             | "0x11c058c3efbf53939fb..."  |
| **reporter**    | User/company who reported the scam first                     | "MyCrypto"                  |
| **ip**          | IP address of the reporter                                   | "198.54.117.200"            |
| **status**      | If the scam is currently active, inactive or has been taken offline | "Offline"                   |
