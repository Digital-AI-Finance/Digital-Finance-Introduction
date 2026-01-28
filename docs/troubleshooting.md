# Troubleshooting Guide

This guide helps you resolve common issues encountered while working through the Digital Finance course. Most problems can be solved with quick fixes; if you're stuck, follow the "Getting Help" section at the end.

---

## Table of Contents

1. [Google Colab Issues](#google-colab-issues)
2. [Python and Package Issues](#python-and-package-issues)
3. [Blockchain and Web3 Issues](#blockchain-and-web3-issues)
4. [Data and API Issues](#data-and-api-issues)
5. [Notebook Functionality Issues](#notebook-functionality-issues)
6. [Getting Help](#getting-help)

---

## Google Colab Issues

### Notebook Won't Open

**Problem:** Clicking the Colab link produces an error or blank page.

**Solution:**
1. Check your internet connection
2. Try opening in an incognito/private browser window
3. Clear browser cache and cookies, then retry
4. If the link is broken, go to [Google Colab](https://colab.research.google.com) directly and upload the `.ipynb` file manually
5. Try a different browser (Chrome is recommended)

**Why this happens:** Browser extensions can interfere with Colab; incognito mode bypasses them.

---

### "Runtime Not Connected" or Runtime Keeps Disconnecting

**Problem:** You see "Runtime disconnected" message or the runtime stops responding.

**Solution:**
1. Click "Reconnect" button in the top-right corner
2. If that doesn't work, click "Runtime" → "Restart runtime"
3. After restarting, re-run cells from the beginning (don't skip cells)
4. If frequent disconnections continue, try a different time when Colab servers are less busy

**Prevention Tips:**
- Don't leave Colab idle for extended periods (Colab disconnects after ~30 minutes of inactivity)
- Close other tabs and applications to reduce memory usage
- Avoid running multiple Colab notebooks simultaneously

**Why this happens:** Colab has resource limits and timeouts. Heavy computations or memory usage can trigger disconnections.

---

### "Module Not Found" Error After Opening Notebook

**Problem:** You get `ModuleNotFoundError: No module named 'X'` when running a cell.

**Solution:**
1. **Always run the pip install cell first** - There's typically a setup cell at the top of each notebook with a code block starting with `!pip install`
2. Make sure you see `Successfully installed...` message after running the install cell
3. If the install runs but you still get the error, restart the runtime and re-run the install cell:
   - Click "Runtime" → "Restart runtime"
   - Then run the install cell again
4. If the error persists, you may need to install a specific version. See [Python and Package Issues](#python-and-package-issues) below

**Example error:**
```
ModuleNotFoundError: No module named 'web3'
```

**Correct fix:**
```python
!pip install web3
```

---

### "Permission Denied" or Authentication Errors

**Problem:** You get errors about authentication or permissions when the notebook tries to access Google Drive or other services.

**Solution:**
1. Click the authentication link or "Authorize" button that appears
2. Sign in with your Google account
3. Grant permissions to Colab to access your resources
4. Re-run the cell that failed

**Why this happens:** Colab notebooks that access Google Drive or Google Sheets require explicit permission from you.

---

### Notebook is Very Slow or Cells Take Forever to Run

**Problem:** Cells execute but take much longer than expected.

**Solution:**
1. Check if you're using a GPU (optional for some notebooks):
   - Click "Runtime" → "Change runtime type"
   - Select "GPU" from the Hardware accelerator dropdown
   - Click "Save"
2. Try restarting the runtime and re-running cells
3. Check your internet connection
4. Close other applications to free up system resources
5. Check if Colab is experiencing server issues (try a different notebook)

**Why this happens:** Colab's free tier has variable performance depending on demand and your available resources.

---

### Cannot Save/Download Output or Charts

**Problem:** Charts won't display in notebook or you can't download results.

**Solution:**
1. **For charts not displaying:** Run the cell again. If it still doesn't show, try:
   - Click "Runtime" → "Restart runtime"
   - Re-run all cells from the top

2. **For downloading files:**
   - Use the download button that appears next to output files
   - Or use Colab's file manager: Click the folder icon on the left sidebar
   - Right-click files and select "Download"

3. **If nothing appears:** The cell may have errors. Check the output area for error messages (often in red text).

---

## Python and Package Issues

### Package Installation Fails

**Problem:** When running `!pip install`, you get errors or `pip` doesn't find the package.

**Solution:**
1. For **connection issues** (timeout, network error):
   ```python
   !pip install --upgrade pip
   !pip install --timeout 60 package_name
   ```

2. For **package not found**:
   - Verify the exact package name (capitalization matters)
   - For Web3: use `web3` (lowercase)
   - For data science: check [PyPI](https://pypi.org) for correct spelling

3. For **version conflicts**:
   ```python
   !pip install --upgrade package_name
   ```

4. Try installing from a different source:
   ```python
   !pip install --index-url https://pypi.org/simple/ package_name
   ```

**Common package names used in this course:**
- `web3` - Ethereum interaction
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib`, `seaborn` - Data visualization
- `scikit-learn` - Machine learning
- `requests` - HTTP requests
- `yfinance` - Financial data

---

### Import Errors After Installation

**Problem:** Package installed successfully but `import x` still fails.

**Solution:**
1. **Restart the runtime** (very important):
   - Click "Runtime" → "Restart runtime"
   - Then re-run your import statements

2. If the error persists:
   ```python
   # Reinstall after restarting
   !pip install --upgrade package_name
   ```

3. Check for typos:
   ```python
   # CORRECT:
   import pandas as pd
   from web3 import Web3

   # INCORRECT (will fail):
   import panda as pd  # wrong name
   from web3 import web3  # wrong capitalization
   ```

**Why this happens:** Colab caches imports; restarting the runtime clears the cache.

---

### Version-Specific Errors

**Problem:** You get errors about incompatible versions or deprecated features.

**Solution:**
1. For **Web3.py specifically**:
   ```python
   !pip install web3==6.0.0
   ```

2. Check what version is installed:
   ```python
   import web3
   print(web3.__version__)
   ```

3. If you need a specific version for a notebook, modify the install cell:
   ```python
   !pip install web3==6.11.0  # Exact version
   ```

**Version notes:**
- Web3.py has had API changes; notebooks specify version 6.0+
- Pandas 1.3+ is recommended for stability
- scikit-learn 0.24+ needed for newer features

---

## Blockchain and Web3 Issues

### Cannot Connect to Ethereum Network

**Problem:** Web3 connection fails with errors like `ConnectionError`, `HTTPConnectionPool`, or `ConnectionRefused`.

**Solution:**
1. **Check your internet connection** - Try loading a regular website
2. **Use a public RPC endpoint**:
   ```python
   from web3 import Web3

   # Recommended free endpoints:
   w3 = Web3(Web3.HTTPProvider('https://eth.publicrpc.com'))
   # Or:
   w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))

   # Check connection:
   print(w3.is_connected())  # Should print True
   ```

3. **If still failing**, the RPC endpoint may be rate-limited or down:
   ```python
   # Try another endpoint
   w3 = Web3(Web3.HTTPProvider('https://1rpc.io/eth'))
   ```

4. **Use fallback/cached data** - Most notebooks include hardcoded example data for offline use

**Why this happens:** Public RPC endpoints have usage limits. High-traffic periods may cause rate limiting.

**Free Ethereum RPC endpoints:**
- https://eth.publicrpc.com
- https://rpc.ankr.com/eth
- https://eth-mainnet.g.alchemy.com/v2/demo (limited)
- https://1rpc.io/eth

---

### "Transaction Not Found" or "Block Not Found"

**Problem:** You try to fetch a transaction or block by hash and get `TransactionNotFound` or `BlockNotFound` error.

**Solution:**
1. **Check the hash** - Verify the transaction/block hash is correct (40-64 hexadecimal characters)
2. **Use example data** - Most notebooks include hardcoded transaction/block hashes for reproducibility
3. **Check testnet vs mainnet** - Make sure you're connected to the right network:
   ```python
   from web3 import Web3

   # For Ethereum mainnet:
   w3 = Web3(Web3.HTTPProvider('https://eth.publicrpc.com'))

   # For Sepolia testnet:
   w3 = Web3(Web3.HTTPProvider('https://sepolia-rpc.publicrpc.com'))
   ```

4. **The block may not be synced yet** - If querying recent blocks, wait a few moments and retry

**Why this happens:** Historical data may not be available on all RPC endpoints; testnet/mainnet confusion is common.

---

### Gas Price or Fee Estimation Errors

**Problem:** Getting errors when trying to estimate gas or fetch current gas prices.

**Solution:**
1. **Use example data from the notebook** - Notebooks typically include hardcoded gas prices and fee estimates
2. **Handle network fluctuations**:
   ```python
   from web3 import Web3

   w3 = Web3(Web3.HTTPProvider('https://eth.publicrpc.com'))

   try:
       gas_price = w3.eth.gas_price
       print(f"Current gas price: {gas_price} wei")
   except Exception as e:
       print(f"Could not fetch live gas price: {e}")
       # Use example instead
       gas_price = 30 * 10**9  # 30 Gwei (example)
   ```

3. For more reliable pricing, use a dedicated service:
   ```python
   import requests

   response = requests.get('https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken')
   # Note: requires free Etherscan API key
   ```

---

### Wallet or Private Key Issues

**Problem:** Errors related to wallet creation, signing, or private key handling.

**Solution:**
1. **Never paste your real private key** - Even in notebooks you write yourself
2. **For generating example wallets** (safe):
   ```python
   from eth_account import Account

   # Generate a NEW account (example only, not for real funds)
   account = Account.create()
   print(f"Address: {account.address}")
   print(f"Private Key: {account.key.hex()}")
   ```

3. **For signing with a key**:
   ```python
   from eth_account import Account
   from web3 import Web3

   # Example: Create account from private key (for demo purposes only)
   # Private key should be stored securely, never hardcoded
   private_key = "0x..." # NEVER share this
   account = Account.from_key(private_key)

   # Sign a message
   message = "Hello, Ethereum"
   signed = account.sign_message(Web3.keccak(text=message))
   ```

4. **If you get "Invalid private key" errors**:
   - Ensure key is 66 characters (0x + 64 hex digits)
   - Remove any spaces or special characters
   - Ensure it starts with `0x`

**Security Warning:** Never use real private keys in notebooks or share them. These notebooks are for education only.

---

## Data and API Issues

### API Rate Limiting

**Problem:** You get `429 Too Many Requests` or similar rate-limit errors.

**Solution:**
1. **Wait and retry** - Respect API limits by pausing before retry:
   ```python
   import time
   import requests

   max_retries = 3
   for attempt in range(max_retries):
       try:
           response = requests.get('https://api.example.com/data')
           break
       except requests.exceptions.HTTPError as e:
           if e.response.status_code == 429:
               wait_time = 5 * (attempt + 1)  # 5, 10, 15 seconds
               print(f"Rate limited. Waiting {wait_time} seconds...")
               time.sleep(wait_time)
           else:
               raise
   ```

2. **Use cached/fallback data** - Notebooks include example datasets for this reason:
   ```python
   # Instead of:
   # data = fetch_live_data()

   # Use included data:
   data = pd.read_csv('example_data.csv')
   ```

3. **Get a free API key** (for services that offer them):
   - Etherscan: https://etherscan.io/apis (free tier available)
   - YFinance: No key needed, but has rate limits
   - CoinGecko: https://www.coingecko.com/en/api (free tier)

---

### Data is Stale or Outdated

**Problem:** Notebook results don't match current market data.

**Solution:**
1. **This is intentional** - Many notebooks use historical data for reproducibility. You'll get the same results every time, which is good for learning.

2. **To fetch current data**:
   ```python
   import yfinance as yf

   # Get latest Bitcoin price
   btc = yf.Ticker("BTC-USD")
   current_price = btc.history(period='1d')['Close'].iloc[-1]
   print(f"Current BTC price: ${current_price:.2f}")
   ```

3. **For Ethereum data**:
   ```python
   from web3 import Web3

   w3 = Web3(Web3.HTTPProvider('https://eth.publicrpc.com'))

   # Get latest block number
   latest_block = w3.eth.block_number
   print(f"Latest block: {latest_block}")
   ```

---

### Missing or Broken Data Files

**Problem:** Notebook can't find a CSV file or external data source.

**Solution:**
1. **If data should be in the notebook**, it's typically loaded this way:
   ```python
   import pandas as pd

   # Check if file exists
   import os
   if os.path.exists('data.csv'):
       df = pd.read_csv('data.csv')
   else:
       print("File not found")
   ```

2. **Download external data**:
   ```python
   import requests
   import pandas as pd
   from io import StringIO

   # Download from URL
   url = 'https://example.com/data.csv'
   response = requests.get(url)
   df = pd.read_csv(StringIO(response.text))
   ```

3. **Use fallback/example data**:
   ```python
   # If download fails, use example
   try:
       df = pd.read_csv('https://example.com/data.csv')
   except:
       # Use included example
       df = pd.DataFrame({
           'date': ['2024-01-01', '2024-01-02'],
           'price': [100, 105]
       })
   ```

---

## Notebook Functionality Issues

### Charts or Plots Not Displaying

**Problem:** Code runs without error but no chart appears.

**Solution:**
1. **For Matplotlib** (most common):
   ```python
   import matplotlib.pyplot as plt

   plt.figure(figsize=(10, 6))
   plt.plot([1, 2, 3], [1, 4, 9])
   plt.title("Example Chart")
   plt.xlabel("X")
   plt.ylabel("Y")
   plt.show()  # Add this line
   ```

2. **For Plotly**:
   ```python
   import plotly.express as px

   fig = px.scatter(df, x='x_col', y='y_col')
   fig.show()  # Must call show()
   ```

3. **If still not displaying**:
   - Restart runtime: "Runtime" → "Restart runtime"
   - Re-run the cell
   - Check browser console for JavaScript errors (F12)

---

### Dataframe Display Issues (Pandas)

**Problem:** Large dataframes display strangely or truncate output.

**Solution:**
1. **View first/last rows**:
   ```python
   df.head()      # First 5 rows
   df.tail()      # Last 5 rows
   df.head(20)    # First 20 rows
   ```

2. **Get dataframe info**:
   ```python
   df.shape           # Rows and columns
   df.info()          # Data types and non-null counts
   df.describe()      # Statistical summary
   ```

3. **Configure display options**:
   ```python
   import pandas as pd

   # Show more columns
   pd.set_option('display.max_columns', None)
   # Show wider columns
   pd.set_option('display.max_colwidth', None)
   # Reset to defaults
   pd.reset_option('display.max_columns')
   ```

---

### Variable Errors: "Name 'X' is Not Defined"

**Problem:** You get `NameError: name 'X' is not defined`.

**Solution:**
1. **The cell defining the variable hasn't been run** - Always run cells from top to bottom
   - Restart runtime: "Runtime" → "Restart runtime"
   - Re-run all cells from the beginning

2. **Typo in variable name**:
   ```python
   # Wrong:
   print(my_variable)  # If defined as my_var

   # Check what variables exist:
   print(dir())  # Shows all defined variables
   ```

3. **Check spelling and capitalization**:
   ```python
   # These are different:
   My_Variable
   my_variable
   myVariable
   ```

---

### Calculations Giving Unexpected Results

**Problem:** Math results seem wrong or too large/small.

**Solution:**
1. **Check decimal places and scientific notation**:
   ```python
   # Print with formatting
   value = 0.0000001
   print(f"Value: {value}")           # May show in scientific notation
   print(f"Value: {value:.10f}")      # Show 10 decimal places
   ```

2. **Check units** (very common in blockchain):
   ```python
   from web3 import Web3

   # Web3 returns values in wei (smallest unit)
   balance_wei = 1000000000000000000
   balance_eth = Web3.from_wei(balance_wei, 'ether')

   print(f"Wei: {balance_wei}")
   print(f"ETH: {balance_eth}")
   ```

3. **Common unit conversions**:
   ```python
   # Ethereum:
   1 ETH = 10^18 wei
   1 Gwei = 10^9 wei

   # Bitcoin:
   1 BTC = 10^8 satoshis
   ```

4. **Check for NaN or Infinity**:
   ```python
   import numpy as np

   print(np.isnan(value))  # Is it NaN?
   print(np.isinf(value))  # Is it infinity?
   ```

---

### Timeout or "Resource Exhausted" Errors

**Problem:** Long computations fail with timeout or resource limit errors.

**Solution:**
1. **Check computation complexity** - Some calculations are intentionally simplified for teaching:
   ```python
   # If a loop takes too long, reduce iterations:
   for i in range(10):      # Start with small number
       # Do work
   ```

2. **Use vectorized operations** (much faster):
   ```python
   import pandas as pd

   # Slow:
   for i in range(len(df)):
       df.iloc[i, 0] = df.iloc[i, 0] * 2

   # Fast:
   df.iloc[:, 0] = df.iloc[:, 0] * 2
   # Or:
   df = df.apply(lambda x: x * 2)
   ```

3. **Optimize memory usage**:
   ```python
   # Use chunks for large datasets
   for chunk in pd.read_csv('large_file.csv', chunksize=1000):
       process_chunk(chunk)
   ```

4. **Restart runtime** to free memory:
   - "Runtime" → "Restart runtime"
   - Close other Colab tabs

---

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide** - Search for your error message
2. **Read error messages carefully** - They often tell you exactly what's wrong
3. **Try the suggested solutions above** - Most issues are covered
4. **Restart the runtime** - Fixes 50% of Colab issues
5. **Try a different time** - Colab servers may be temporarily overloaded

---

### How to Report an Issue

When you need help, include:

1. **The exact error message** (copy the full red error text):
   ```
   Bad: "It doesn't work"
   Good: "ModuleNotFoundError: No module named 'web3'"
   ```

2. **Which notebook and cell** you were running:
   ```
   Example: "Day 3 notebook, Cryptography cell, the hash() function"
   ```

3. **What you tried** to fix it:
   ```
   Example: "Restarted runtime, re-ran install cell"
   ```

4. **Screenshots** of the error (optional but helpful):
   - Use Ctrl+Shift+S (or Cmd+Shift+S on Mac) to take a screenshot
   - Include the browser address bar and error message

---

### Where to Get Help

**For course content questions:**
- Check the course README.md in the GitHub repository
- Review the relevant day's lecture slides
- Check the [Digital Finance Glossary](./glossary.md) for term definitions

**For notebook/technical issues:**
- Post in the course discussion forum (if available)
- Check the course GitHub repository Issues tab
- Contact the instructor with detailed information (error message, notebook name, exact step)

**For general Python/Jupyter help:**
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html)
- [Stack Overflow](https://stackoverflow.com) - Search for your error message
- [Python documentation](https://docs.python.org/)

**For blockchain-specific issues:**
- [Web3.py documentation](https://web3py.readthedocs.io/)
- [Ethereum Stack Exchange](https://ethereum.stackexchange.com/)
- [Etherscan Blog](https://blog.etherscan.io/) for network status

---

## Quick Reference: Common Error Solutions

| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| `ModuleNotFoundError` | Package not installed | Run `!pip install package_name` |
| `ConnectionError` | Network or RPC offline | Try different RPC endpoint |
| `TransactionNotFound` | Wrong transaction hash or testnet/mainnet mismatch | Check hash, verify network |
| `NameError: name 'X' is not defined` | Variable not yet created | Run cells from top to bottom |
| `Runtime disconnected` | Colab timeout or resource limit | Click "Reconnect" or "Restart runtime" |
| `ModuleNotFoundError` after install | Runtime not restarted | Restart runtime after installing |
| Chart doesn't display | Missing `.show()` or need restart | Add `plt.show()` or restart runtime |
| Permission denied | Auth required | Click auth link and grant permissions |
| Rate limited | Too many API requests | Wait and retry, or use cached data |

---

## Preventing Future Issues

1. **Always run cells from top to bottom** - Don't skip cells
2. **Run the pip install cell first** - Before any other code
3. **Restart runtime after installing packages** - Then re-run cells
4. **Save your work** - Colab auto-saves, but can download notebooks too
5. **Use example data when available** - More reliable than live APIs
6. **Check your internet connection** - Before assuming code is wrong
7. **Read error messages carefully** - They usually point to the solution

---

**Last Updated:** 2026-01-28
**Course Version:** 1.0
