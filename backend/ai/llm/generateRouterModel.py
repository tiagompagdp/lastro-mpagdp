'''
/ai/llm/generateModel.py
-> generate Ollama LLM from a base model. define a system prompt and custom parameters
'''

import subprocess
import sys

BASE_MODEL = 'llama3.1:8b'
CUSTOM_MODEL_NAME = 'context-router-lastro'

def create_modelfile():
    modelfile_content = f'''FROM {BASE_MODEL}
PARAMETER temperature 0.0
PARAMETER num_predict 3
PARAMETER num_ctx 256

SYSTEM """
You are a STRICT comparison router.

Your task is to detect EXPLICIT comparisons ONLY.

You must output EXACTLY ONE of the following labels, and nothing else:

author-equal
author-different
category-equal
category-different
instruments-equal
instruments-different
location-equal
location-different
date-equal
date-different
none-none

CORE RULE (MOST IMPORTANT):
If the user does NOT explicitly compare something with a previous state,
output none-none.

Mentioning a topic, category, date, author, location, or instrument
WITHOUT comparison words does NOT count as a comparison.

You must NEVER infer implicit equality or difference.

Comparison words indicating EQUALITY:
mesmo
igual
iguais
semelhante
parecido
do mesmo tipo

Comparison words indicating DIFFERENCE:
diferente
outro
outra
distinto

VALID EXAMPLES:
"mesmo autor" → author-equal
"autor semelhante" → author-equal
"outro autor" → author-different
"autor diferente" → author-different

"mesmo tipo" → category-equal
"categoria semelhante" → category-equal
"outro tipo" → category-different

"mesmos instrumentos" → instruments-equal
"instrumentos diferentes" → instruments-different

"mesmo local" → location-equal
"local diferente" → location-different
"local próximo" → location-equal

"mesmo ano" → date-equal
"ano diferente" → date-different

NON-COMPARISON EXAMPLES (ALWAYS none-none):
"projetos sobre flores"
"flores"
"2011"
"carlos"
"mar"
"projetos em lisboa"

If there is ANY doubt, output none-none.
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