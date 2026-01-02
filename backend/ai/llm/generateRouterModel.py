'''
/ai/llm/generateModel.py
-> generate Ollama LLM from a base model. define a system prompt and custom parameters
'''

import subprocess
import sys

BASE_MODEL = 'gemma2:2b'
CUSTOM_MODEL_NAME = 'context-router-lastro'

def create_modelfile():
    modelfile_content = f'''FROM {BASE_MODEL}
PARAMETER temperature 0.0
PARAMETER num_predict 5
PARAMETER num_ctx 1024

SYSTEM """
Only output: author-equal, author-different, category-equal, category-different, instruments-equal, instruments-different, location-equal, location-different, date-equal, date-different, or none-none

NEVER output: author-similar, author-like, category-similar, or any word other than equal/different

mesmo autor → author-equal
autor semelhante → author-equal (NOT author-similar)
autor parecido → author-equal (NOT author-like)
autor igual → author-equal
autor diferente → author-different
outro autor → author-different
mesmo tipo → category-equal
categoria semelhante → category-equal (NOT category-similar)
mesmo ano → date-equal
mesmos instrumentos → instruments-equal
local diferente → location-different
local próximo → location-equal
carlos → none-none
mar → none-none
"""
'''
    
    with open('Modelfile', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)

# create_modelfile_codellama7b_optimized()
def create_model():    
    try:
        result = subprocess.run(
            ['ollama', 'create', CUSTOM_MODEL_NAME, '-f', 'Modelfile'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Model '{CUSTOM_MODEL_NAME}' created successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: 'ollama' not found. Install from https://ollama.ai")
        sys.exit(1)

def main():
    print("Creating Ollama custom model...\n")
    create_modelfile()
    create_model()

if __name__ == '__main__':
    main()