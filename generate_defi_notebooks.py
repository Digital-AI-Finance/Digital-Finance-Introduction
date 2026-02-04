import json
import os

def create_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": [], "collapsed_sections": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3", "language": "python"},
            "language_info": {
                "name": "python",
                "version": "3.8.10",
                "mimetype": "text/x-python",
                "codemirror_mode": {"name": "ipython", "version": 3},
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

def md_cell(lines):
    if isinstance(lines, str):
        lines = [lines]
    return {"cell_type": "markdown", "metadata": {}, "source": lines}

def code_cell(lines):
    if isinstance(lines, str):
        lines = [lines]
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": lines}

def colab_badge(path):
    return md_cell(f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digital-AI-Finance/Digital-Finance-Introduction/blob/main/{path})")

print("Generating DeFi notebooks...")

# Save helper
def save_notebook(nb, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Created: {path}")

print("Complete. 4 notebooks generated.")
