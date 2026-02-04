import json
import os

def save_nb(path, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"}
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [text] if isinstance(text, list) else [text]}

def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [text] if isinstance(text, list) else [text]}

cells = [
    md("[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digital-AI-Finance/Digital-Finance-Introduction/blob/main/day_04/notebooks/NB08_Smart_Contracts.ipynb)"),
    md("# NB08: Smart Contract Interaction"),
    code("!pip install -q web3"),
    code("from web3 import Web3\nprint('Ready')")
]

save_nb(r'day_04\notebooks\NB08_Smart_Contracts.ipynb', cells)
print("NB08 created")
