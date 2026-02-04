import json
import os

def write_notebook(filepath, cells):
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

# Create cells for Notebook 1
cells = [
    {"cell_type": "markdown", "metadata": {}, "source": "# Money and Ledgers Simulation\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digital-AI-Finance/Digital-Finance-Introduction/blob/main/day_01/notebooks/NB01_Money_Ledgers.ipynb)"},
    {"cell_type": "markdown", "metadata": {}, "source": "## Learning Objectives\n\nBy the end of this notebook, you will understand:\n1. How a simple ledger system works\n2. How transactions are recorded\n3. The double-spending problem\n4. How a central authority prevents double-spending"},
    {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "from datetime import datetime\n\nledger = []\nbalances = {'Alice': 100, 'Bob': 50, 'Charlie': 75}\n\nprint('Initial Balances:')\nfor person, amount in balances.items():\n    print(f'  {person}: ${amount}')"}
]

write_notebook('day_01/notebooks/NB01_Money_Ledgers.ipynb', cells)
print("Created NB01")
