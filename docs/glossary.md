# Digital Finance Glossary

A concise reference guide for key terms used throughout the Digital Finance course. Definitions are written for BSC-level students with no prior finance or technology prerequisites.

---

## A

### AML (Anti-Money Laundering)

Regulatory procedures and technology systems designed to detect and prevent the use of financial systems for illegal purposes, such as hiding proceeds from crime or terrorism. In digital finance, AML compliance typically involves transaction monitoring, suspicious activity reporting, and customer screening. Both traditional and crypto platforms must implement AML controls to operate legally.

### AMM (Automated Market Maker)

A type of decentralized exchange that uses a mathematical formula (usually constant-product formula: x × y = k) to determine asset prices and facilitate trades automatically, rather than relying on a traditional order book. Users called liquidity providers deposit equal values of two assets into a pool and earn fees when others trade against the pool. Enables permissionless trading but exposes liquidity providers to impermanent loss.

### API (Application Programming Interface)

A standardized set of rules that allows software applications to communicate with each other and request services. In digital finance, APIs enable FinTech companies to access bank data, initiate payments, or interact with blockchain networks without building infrastructure from scratch. Open banking APIs, for example, allow third-party apps to read customer account information with permission.

---

## B

### BaaS (Banking-as-a-Service)

A business model where traditional banks provide infrastructure and regulatory licenses to non-bank companies, allowing them to offer financial products (checking accounts, lending, payments) without becoming regulated banks themselves. The non-bank company handles customer relationships and user experience while the bank manages deposits and regulatory compliance. Enables rapid FinTech scaling.

### Blockchain

A distributed digital ledger that records transactions in a chain of cryptographically linked blocks. All participants maintain an identical copy of the ledger, and new transactions are validated through consensus mechanisms (like Proof of Work or Proof of Stake) rather than by a single authority. Enables transparent, tamper-resistant record-keeping without requiring trust in a central intermediary.

---

## C

### CBDC (Central Bank Digital Currency)

Digital currency issued and backed by a country's central bank. Unlike cryptocurrencies, CBDCs are legal tender and carry the government's full credit. Can be account-based (like a digital bank account) or token-based (like digital cash). Intended to modernize payments and financial system infrastructure while maintaining central bank control and monetary policy effectiveness.

### CEX (Centralized Exchange)

A cryptocurrency exchange operated by a company that holds user funds and controls the trading platform. Users deposit cryptocurrency or fiat money with the exchange, which holds these assets in custody while executing trades. CEXs typically offer better user experience and liquidity than decentralized alternatives but require trust in the exchange's security and solvency (as seen in exchange collapses like FTX).

### Consensus (PoW, PoS)

The mechanism by which a blockchain network reaches agreement on which transactions are valid and should be added to the ledger. Proof of Work (PoW) requires computational puzzle-solving and consumes significant energy (used by Bitcoin). Proof of Stake (PoS) requires validators to hold and risk cryptocurrency, using far less energy (adopted by Ethereum). Both ensure security by making dishonest behavior costly.

### Cryptocurrency

Digital currency secured by cryptography rather than backed by a government or physical commodity. Transactions are recorded on a blockchain and verified by the network rather than a bank. Unlike stablecoins, cryptocurrencies like Bitcoin and Ethereum are typically volatile in value. Can be used as a medium of exchange, store of value, or unit of account.

### Custodial Wallet

A cryptocurrency wallet where a third party (exchange, service provider, or bank) holds private keys and funds on behalf of the user. The user accesses funds through the third party's interface but does not directly control the keys. Easier to use and recover if forgotten, but requires trust in the custodian and exposes users to custodian insolvency risk.

---

## D

### DAO (Decentralized Autonomous Organization)

An organization governed entirely by smart contracts and token-holder voting, with no central management structure. Decisions (such as spending treasury funds or changing protocol parameters) are made through on-chain voting by governance token holders. Enables permissionless participation but faces challenges with voter apathy, plutocratic concentration, and governance attacks.

### DEX (Decentralized Exchange)

A cryptocurrency exchange where users trade peer-to-peer through smart contracts rather than entrusting funds to a company. Users retain control of their private keys and assets throughout the trading process. DEXs offer greater privacy and no counterparty risk, but typically have lower liquidity, higher slippage, and worse user experience than centralized exchanges.

### DeFi (Decentralized Finance)

Financial services (lending, borrowing, trading, insurance, derivatives) built on blockchain platforms and smart contracts, operating without traditional financial intermediaries. DeFi protocols are permissionless (open to anyone), transparent (all transactions visible on-chain), and composable (protocols can be chained together). Replaces institutional trust with cryptographic and economic incentives.

---

## F

### FinTech (Financial Technology)

Technology-driven innovation that improves, automates, or disintermediates traditional financial services while operating within the existing regulatory system. Examples include digital payments, robo-advisors, peer-to-peer lending platforms, and neobanks. FinTech typically augments existing financial infrastructure (banking rails, payment networks) rather than replacing it.

---

## G

### Gas Fee

The cost to execute a transaction or smart contract on certain blockchains (notably Ethereum). Measured in the network's native token and paid to validators/miners for processing computational work. Gas fees fluctuate based on network congestion; when many users want to transact, fees increase. High gas fees can make small transactions uneconomical, limiting blockchain adoption for retail payments.

### Governance Token

A cryptocurrency token that grants voting rights on protocol decisions, such as parameter changes, fee structures, or treasury allocation. Governance tokens are typically distributed to early users and developers to decentralize control. Holders with more tokens have more voting power, creating a plutocratic risk where whale token holders can dictate outcomes.

---

## I

### Impermanent Loss

The loss experienced by liquidity providers in automated market makers (AMMs) when the price ratio of deposited assets changes significantly. If a provider deposits equal values of two assets and their price ratio diverges, the provider would have been better off holding the assets rather than providing liquidity (even accounting for trading fees earned). Most relevant when asset volatility is high.

---

## K

### KYC (Know Your Customer)

Regulatory procedure requiring financial institutions to verify customer identity and assess the purpose of their financial activity. KYC checks involve requesting government-issued ID, proof of address, and sometimes information about income sources. Mandatory in traditional finance and increasingly required in regulated FinTech; creates friction and exclusion but enables fraud prevention and regulatory compliance.

---

## L

### Layer 2

Blockchain scaling solutions that process transactions off the main blockchain (layer 1) and periodically settle results back to the main chain, reducing congestion and lowering gas fees. Examples include Optimistic Rollups (Optimism, Arbitrum) and Zero-Knowledge Rollups (zkSync). Enable much higher transaction throughput than layer 1 but introduce different trust and security assumptions.

### Liquidity Pool

A collection of cryptographic assets deposited by users (liquidity providers) into a smart contract to enable peer-to-peer trading through an automated market maker. Traders swap tokens against the pool, paying fees that are distributed proportionally to liquidity providers. Pools function like market makers but are automated rather than managed by humans.

---

## N

### NFT (Non-Fungible Token)

A cryptographic token that represents unique, non-interchangeable ownership of a digital or physical asset. Unlike fungible tokens (like USD stablecoins, where all units are identical), each NFT is distinct and identified by unique metadata. Used for digital art, collectibles, in-game items, and digital identity; enables verifiable ownership and transfer of digital assets.

### Non-Custodial Wallet

A cryptocurrency wallet where the user holds the private keys and has exclusive control over funds. No third party can access or move the user's assets without the private key. Offers true ownership and privacy but requires users to manage keys securely; loss or compromise of private keys results in irreversible loss of funds.

---

## O

### Open Banking

A regulatory and technical framework that allows third-party developers to access banking data and services (via APIs) with customer permission. Enables new companies to build financial products using bank data without becoming banks themselves. Drives FinTech innovation by disintermediating banks and lowering barriers to entry for financial services.

### Oracle

A service that brings external data (prices, weather, sports scores, etc.) onto a blockchain so smart contracts can use that information. Oracles are necessary because blockchains cannot directly access off-chain data. Decentralized oracle networks (like Chainlink) use multiple data providers and consensus mechanisms to avoid having a single oracle become a point of failure or manipulation.

---

## R

### RegTech (Regulatory Technology)

Technology solutions designed to help organizations comply with financial regulations more efficiently, such as transaction monitoring, identity verification, sanctions screening, and reporting. RegTech reduces compliance costs and improves detection of suspicious activity. Used by both traditional financial institutions and increasingly by crypto platforms.

---

## S

### Smart Contract

Self-executing code deployed on a blockchain that automatically executes terms when conditions are met, without requiring a human intermediary. Smart contracts are immutable (cannot be changed after deployment) and transparent (all can view the code). Enable DeFi protocols but are vulnerable to coding bugs, security exploits, and the oracle problem (inability to access external data directly).

### Stablecoin

A cryptocurrency designed to maintain a stable value relative to another asset (usually the US dollar) through one of three mechanisms: (1) fiat-backed (backed 1:1 by USD in a bank account), (2) crypto-collateralized (over-collateralized with other cryptocurrencies), or (3) algorithmic (stabilized through automated market mechanisms). Enable cryptocurrency's transparency and speed while reducing volatility, making stablecoins the most crypto-friendly innovation for traditional finance integration.

---

## T

### Tokenization

The process of converting rights or value associated with an asset into a digital token on a blockchain. A tokenized asset can be divided into smaller units, traded instantly, and transferred globally without intermediaries. Examples include tokenized real estate, bonds, commodities, or even income streams. Enables efficient markets for assets historically illiquid.

---

## W

### Wallet

A software application or physical device that stores cryptographic keys and enables users to send, receive, and manage cryptocurrency. Wallets display balances and transaction history but do not actually store coins (which exist on the blockchain). Two types: custodial (third party holds keys) and non-custodial (user holds keys). Private key security is critical; loss means permanent asset loss.

---

## Y

### Yield Farming

A strategy where users deposit cryptocurrency into DeFi protocols to earn returns through trading fees (liquidity provision), interest (lending), or governance incentives. Yield farmers often move capital between protocols chasing highest returns. Introduces leverage, smart contract risk, and impermanent loss to ordinary users, but enables bootstrapping of DeFi protocols through token incentives.

---

## Glossary Notes

### How to Use This Glossary

- Terms are organized alphabetically by first letter
- Cross-references (in italics) link related concepts within the glossary
- Definitions are written for students with no assumed prior finance or technology knowledge
- Each definition includes the "why this matters" context for digital finance

### Terms Organized by Theme

**Core Blockchain Concepts**: Blockchain, Consensus (PoW, PoS), Cryptocurrency, Smart Contract, Oracle

**Digital Assets**: Stablecoin, Tokenization, NFT, Cryptocurrency, CBDC

**Decentralized Finance**: DeFi, DEX, Liquidity Pool, AMM, Smart Contract, Yield Farming, Impermanent Loss, Governance Token, DAO, Layer 2

**Centralized Finance & FinTech**: FinTech, CEX, API, Open Banking, BaaS

**Wallets & Custody**: Wallet, Custodial Wallet, Non-Custodial Wallet

**Regulation & Compliance**: KYC, AML, RegTech, CBDC

**Fees & Economics**: Gas Fee, AMM, Liquidity Pool, Impermanent Loss, Yield Farming
