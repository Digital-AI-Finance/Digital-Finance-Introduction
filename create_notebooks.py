import json
import os

os.makedirs('day_05/notebooks', exist_ok=True)
os.makedirs('day_06/notebooks', exist_ok=True)

def mk_md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': [text]}

def mk_code(code):
    return {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [code]}

def mk_colab_badge(path):
    return {
        'cell_type': 'markdown',
        'metadata': {'id': 'view-in-github', 'colab_type': 'text'},
        'source': [f'<a href="https://colab.research.google.com/github/Digital-AI-Finance/Digital-Finance-Introduction/blob/main/{path}" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>']
    }

print("Creating notebooks...")
print("This will take a moment...")
