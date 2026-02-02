'''
/ai/llm/generateModel.py
-> generate Ollama LLM from a base model. define a system prompt and custom parameters
'''

import subprocess
import sys

BASE_MODEL = 'llama3.2:3b'
CUSTOM_MODEL_NAME = 'context-router-lastro'

def create_modelfile():
    modelfile_content = f'''FROM {BASE_MODEL}
PARAMETER temperature 0.0
PARAMETER num_predict 10
PARAMETER num_ctx 1024

SYSTEM """
Classify query intent. Output ONE label only.

Labels:
- author-equal
- author-different
- category-equal
- category-different
- instruments-equal
- instruments-different
- location-equal
- location-different
- date-equal
- date-different
- none-none

Guidelines:
- Return a `-equal` or `-different` ONLY if the user explicitly uses comparison words: "mesmo", "diferente", "parecido", "outro", "como".
- NEVER return `-different` or `-equal` for a bare name, location, or search term alone. Those are always `none-none`.
- Output exactly ONE label and nothing else.

Examples (COMPARISON - returns -equal or -different):
"mesmo autor" -> author-equal
"autor diferente" -> author-different
"outro autor" -> author-different
"mais deste autor" -> author-equal
"mais deste criador" -> author-equal
"mesma categoria" -> category-equal
"categoria diferente" -> category-different
"vídeos parecidos" -> category-equal
"mais como este" -> category-equal
"mais projetos como este" -> category-equal
"mesmo local" -> location-equal
"local diferente" -> location-different
"noutro sítio" -> location-different
"neste sítio" -> location-equal
"mesma data" -> date-equal
"outros projetos neste ano" -> date-equal
"data diferente" -> date-different
"com os mesmos instrumentos" -> instruments-equal
"instrumentos diferentes" -> instruments-different
"mais do mesmo tipo" -> category-equal
"de tipo diferente" -> category-different

Examples (BARE NAMES/TERMS - returns none-none):
"Maria" -> none-none
"Filipe Sambado" -> none-none
"carlos" -> none-none
"fado" -> none-none
"lisboa" -> none-none
"2023" -> none-none
"guitarra" -> none-none
"vídeos com viola" -> none-none
"mar" -> none-none
"flores e mar" -> none-none
"projetos em Viana do Castelo" -> none-none
"vídeos que falam de maçã" -> none-none
"videos sobre dança" -> none-none
"dança no alentejo" -> none-none
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