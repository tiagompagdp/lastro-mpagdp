'''
/dataGen/queries.py
-> define all the methods for user prompt handle/process
'''

from database.setup import db, executeQueriesSQL, recordInteraction
from ai.llm.setup import queryLLM

# ==================================================
# methods
# ==================================================

def stripQueries(text):

    result = {
        "queries": [],
        "descriptions": [],
        "results": []
    }

    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # isolate query
        if line.startswith('QUERY:'):
            query = line[6:].strip()
            if not query.endswith(';'):
                query += ';'
            result["queries"].append(query)        
        
        # isolate description
        elif line.startswith('DESC:'):
            result["descriptions"].append(line[5:].strip())
        
    return result

# ==================================================
# main
# ==================================================

def handleQuery(data):
    #print(data)
    modelOutput = queryLLM(data["currentPrompt"], data["previousPrompts"])

    #interactionId = recordInteraction(data,modelOutput)

    result = stripQueries(modelOutput)
    result["results"] = executeQueriesSQL(result["queries"])
    #print(result)

    return result