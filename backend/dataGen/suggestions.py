'''
/dataGen/suggestions.py
-> generate suggestions based on a project/video properties
'''

from database.setup import executeQueriesSQL
from dataGen.descriptions import describeDirectSuggestion, describeDisruptiveSuggestion
import random

# ignore when splitting by space
wordsToIgnore = [
    "de", "da", "do", "das", "dos",
    "e", "a", "o", "as", "os",
    "em", "no", "na", "nos", "nas",
    "um", "uma", "uns", "umas",
    "que", "não", "eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas",
    "me", "te", "se", "nos", "vos",
    "meu", "minha", "teu", "tua", "seu", "sua",
    "este", "esta", "esse", "essa", "aquele", "aquela",
    "com", "sem", "para", "por", "sobre", "sob",
    "mas", "mais", "menos", "muito", "pouco",
    "já", "ainda", "sempre", "nunca",
    # Verb "ser"
    "sou", "és", "é", "somos", "sois", "são",
    "era", "eras", "éramos", "éreis", "eram",
    "fui", "foi", "fomos", "fostes", "foram",
    "serei", "será", "seremos", "sereis", "serão",
    "seria", "serias", "seríamos", "seríeis", "seriam",
    "seja", "sejas", "sejamos", "sejais", "sejam",
    "fosse", "fosses", "fôssemos", "fôsseis", "fossem",
    "for", "fores", "formos", "fordes", "forem",
    "ser", "sendo", "sido",
    # Verb "estar"
    "estou", "estás", "está", "estamos", "estais", "estão",
    "estava", "estavas", "estávamos", "estáveis", "estavam",
    "estive", "esteve", "estivemos", "estivestes", "estiveram",
    "estarei", "estará", "estaremos", "estareis", "estarão",
    "estaria", "estarias", "estaríamos", "estaríeis", "estariam",
    "esteja", "estejas", "estejamos", "estejais", "estejam",
    "estivesse", "estivesses", "estivéssemos", "estivésseis", "estivessem",
    "estiver", "estiveres", "estivermos", "estiverdes", "estiverem",
    "estar", "estando", "estado",
]

# 3 direct suggestions, different probabilities
nDirect = 3
directOptions = [
    {"field": "title", "p": 80},
    {"field": "author", "p": 90},
    {"field": "category", "p": 75},
    {"field": "date", "p": 90},
    {"field": "direction", "p": 25},
    {"field": "sound", "p": 5},
    {"field": "production", "p": 5},
    {"field": "support", "p": 5},
    {"field": "assistance", "p": 2},
    {"field": "research", "p": 2},
    {"field": "location", "p": 90},
    {"field": "instruments", "p": 80},
    {"field": "keywords", "p": 50}
]

# 2 diruptive suggestions, same probability
nDisruptive = 2
disruptiveOptions = [
    {"matchField": "author", "excludeField": "category"},
    {"matchField": "author", "excludeField": "location"},
    {"matchField": "author", "excludeField": "instruments"},
    {"matchField": "category", "excludeField": "author"},
    {"matchField": "category", "excludeField": "location"},
    {"matchField": "category", "excludeField": "instruments"},
    {"matchField": "location", "excludeField": "author"},
    {"matchField": "location", "excludeField": "category"},
    {"matchField": "location", "excludeField": "instruments"},
    {"matchField": "instruments", "excludeField": "author"},
    {"matchField": "instruments", "excludeField": "location"},
    {"matchField": "instruments", "excludeField": "category"},
    {"matchField": "author", "excludeField": "date"},
    {"matchField": "date", "excludeField": "author"},
]

# ==================================================
# methods
# ==================================================

def buildQuery(field, project):
    """
    Build a SQL query for a given field and project.
    Strategy:
    1. If field is "date" -> match by year only using LIKE 'year-%'
    2. If value contains ", " -> split and use OR
    3. Otherwise -> try exact LIKE match
    4. If no results -> split by space and use OR (ignoring insignificant words)

    project: The project object to build the query from
    field: The field name to query on
    """
    value = getattr(project, field, None)

    if not value:
        return None

    # Build exclusion clause to exclude current project
    exclude_clause = f" AND id != {project.id}"

    # Special handling for date field
    if field == "date":
        try:
            year = value.strftime('%Y-%m-%d').split('-')[0]
            query = f"SELECT * FROM projects WHERE date LIKE '{year}-%'{exclude_clause}"
            #print(f"[Query - date year] {query}")
            return query
        except:
            return None

    value_str = str(value)

    # Check if value contains ", "
    if ", " in value_str:
        # Split by ", " and create OR conditions
        elements = [elem.strip() for elem in value_str.split(", ")]
        conditions = [f"{field} LIKE '%{elem}%'" for elem in elements if elem]
        where_clause = " OR ".join(conditions)
        query = f"SELECT * FROM projects WHERE ({where_clause}){exclude_clause}"
        #print(f"[Query - comma split] {query}")
        return query
    else:
        # Try exact match first
        query_exact = f"SELECT * FROM projects WHERE {field} LIKE '%{value_str}%'{exclude_clause}"
        #print(f"[Query - exact match] {query_exact}")

        # Execute query to check if it returns results
        results = executeQueriesSQL([query_exact])

        if results and results[0]:  # Has results
            #print(f"[Query - exact match SUCCESS] Found {len(results[0])} results")
            return query_exact
        else:
            #print(f"[Query - exact match FAILED] No results, trying word split...")
            # Split by space and filter out insignificant words
            words = [word.strip() for word in value_str.split(" ")]
            coreWords = [word for word in words if word.lower() not in wordsToIgnore and word]

            if coreWords:
                conditions = [f"{field} LIKE '%{word}%'" for word in coreWords]
                where_clause = " OR ".join(conditions)
                query = f"SELECT * FROM projects WHERE ({where_clause}){exclude_clause}"
                #print(f"[Query - word split] {query}")
                return query
            else:
                # Fallback to exact match if no significant words
                #print(f"[Query - fallback to exact] {query_exact}")
                return query_exact

def getDirect(project):
    options = directOptions.copy()
    selected = []

    while len(selected) < nDirect and options:
        # Select a weighted random option
        weights = [opt["p"] for opt in options]
        chosen = random.choices(options, weights=weights, k=1)[0]
        options.remove(chosen)

        # Build and execute query
        query = buildQuery(chosen["field"], project)
        if query:
            results = executeQueriesSQL([query])
            if results and results[0]:  # Has results
                # Generate dynamic description
                description = describeDirectSuggestion(query, chosen["field"])

                selected.append({
                    "description": description,
                    "projects": results[0]
                })

    #print(f"[getDirect] Final count: {len(selected)} suggestions with results")
    return selected

def getDisruptive(project):
    options = disruptiveOptions.copy()
    selected = []

    while len(selected) < nDisruptive and options:
        # Select a random option
        chosen = random.choice(options)
        options.remove(chosen)

        # Build match query for the matchField
        match_query = buildQuery(chosen["matchField"], project)

        if match_query:
            # Get the exclude field value
            exclude_value = getattr(project, chosen["excludeField"], None)

            if exclude_value:
                # Special handling for date field in exclude
                if chosen["excludeField"] == "date":
                    try:
                        year = exclude_value.strftime('%Y-%m-%d').split('-')[0]
                        exclude_condition = f" AND date NOT LIKE '{year}-%'"
                    except:
                        exclude_condition = ""
                else:
                    exclude_value_str = str(exclude_value)

                    # Handle comma-separated values
                    if ", " in exclude_value_str:
                        elements = [elem.strip() for elem in exclude_value_str.split(", ")]
                        not_conditions = [f"{chosen['excludeField']} NOT LIKE '%{elem}%'" for elem in elements if elem]
                        exclude_condition = " AND " + " AND ".join(not_conditions)
                    else:
                        # Single value
                        exclude_condition = f" AND {chosen['excludeField']} NOT LIKE '%{exclude_value_str}%'"

                # Combine match query with exclude condition
                final_query = match_query.replace(" AND id !=", exclude_condition + " AND id !=")

                results = executeQueriesSQL([final_query])

                if results and results[0]:
                    # Generate dynamic description
                    description = describeDisruptiveSuggestion(chosen["matchField"], chosen["excludeField"])

                    selected.append({
                        "description": description,
                        "projects": results[0]
                    })
            else:
                # No exclude value, use match query alone (less likely but handle gracefully)
                results = executeQueriesSQL([match_query])

                if results and results[0]:
                    # Use direct description as fallback
                    description = describeDirectSuggestion(match_query, chosen["matchField"])

                    selected.append({
                        "description": description,
                        "projects": results[0]
                    })

    return selected

# ==================================================
# main
# ==================================================

def getSuggestions(project):
    """
    Generate suggestions for a project.
    Returns a list of 5 suggestions (3 direct + 2 disruptive),
    each with a description and projects array.
    Suggestions and projects are randomly ordered.
    """
    # Get 3 direct suggestions
    direct = getDirect(project)

    # Get 2 disruptive suggestions
    disruptive = getDisruptive(project)

    # Combine results
    result = direct + disruptive

    # Shuffle projects within each suggestion
    for suggestion in result:
        random.shuffle(suggestion["projects"])

    # Shuffle the suggestions themselves
    random.shuffle(result)
    #result.sort(key=lambda x: len(x["projects"]), reverse=True)

    return result