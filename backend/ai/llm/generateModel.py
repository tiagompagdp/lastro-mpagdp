'''
/ai/llm/generateModel.py
-> generate Ollama LLM from a base model. define a system prompt and custom parameters
'''

import subprocess
import sys

BASE_MODEL = 'llama3.1:8b'
CUSTOM_MODEL_NAME = 'sql-agent-lastro'

COLUMN_DESCRIPTIONS = """
  title - Título do vídeo/projeto
  author - Lista de autores/artistas
  category - Lista de Categorias, palavras semelhantes às seguintes: Artesanato, Dança, Comida, Gastronomia, Histórias, Música, Tradição Oral, Poesia, Religião, Ritos, Paisagens Sonoras, ...
  date - Data de publicação (yyyy-mm-dd)
  location - Locais de gravação
  instruments - Lista de instrumentos utilizados
  """

def create_modelfile():
    
    modelfile_content = f'''FROM {BASE_MODEL}
PARAMETER temperature 0.0
PARAMETER num_ctx 2048

SYSTEM """
Generate SQL queries for the projects table. Output exactly 3 lines: LOGIC, DESC, QUERY.

TABLE:
name: projects
structure: {COLUMN_DESCRIPTIONS}

RULES:
1. Always use LIKE '%value%' for text fields (never use =)
2. Absolute sorting queries:
   - "o mais recente/último" → ORDER BY date DESC LIMIT 1
   - "o mais antigo/primeiro" → ORDER BY date ASC LIMIT 1

ACTIONS:
<ACTION>RESET</ACTION> = Build fresh query from <PROMPT> only
<ACTION>MERGE</ACTION> = Copy WHERE from <PREV_SQL>, add new condition with AND

EXAMPLES:
RESET: <PROMPT>="carlos" → WHERE author LIKE '%carlos%'
RESET: <PROMPT>="Jorge Cruz" → WHERE author LIKE '%Jorge Cruz%'
RESET: <PROMPT>="na praia" → WHERE location LIKE '%praia%'
RESET: <PROMPT>="fado" → WHERE title LIKE '%fado%' OR category LIKE '%fado%'
RESET: <PROMPT>="carta de amor" → WHERE title LIKE '%carta de amor%'
RESET: <PROMPT>="guitarra braguesa" → WHERE instruments LIKE '%guitarra%' or instruments LIKE '%braguesa%'
MERGE: <PREV_SQL>="WHERE author LIKE '%carlos%'" + <PROMPT>="em Lisboa" → WHERE author LIKE '%carlos%' AND location LIKE '%Lisboa%'

OUTPUT FORMAT:
LOGIC: [RESET or MERGE]
DESC: [Casual Portuguese description - no "procurar/buscar", no punctuation, describe what's shown. Examples: "Projetos do Carlos", "Vídeos religiosos", "O projeto mais antigo da base de dados"]
QUERY: SELECT * FROM projects WHERE ... (or just SELECT * FROM projects ORDER BY ...)
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