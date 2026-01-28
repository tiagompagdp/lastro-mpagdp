'''
/dataGen/suggestions.py
-> generate suggestions based on a project/video properties
'''

from database.setup import executeQueriesSQL
from database.models import serializeProjectMinimal
from dataGen.descriptions import describeDirectSuggestion, describeDisruptiveSuggestion
import random
import asyncio
import re
import unicodedata

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
    # {"field": "title", "p": 80},
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

def hasFieldData(field, project):
    """
    Quickly check if a field has usable data without executing queries.
    Returns True if the field exists and has non-empty value.
    """
    value = getattr(project, field, None)
    if not value:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    return True

def isSimilarTitle(title1, title2, threshold=0.60):
    """
    Check if two titles are similar (part of the same series) using accent normalization.
    Matches titles that have the same base (ignoring accents, trailing numbers, and variant markers).
    
    Examples:
    - "improvisação 1" and "improvisação 2" → same base (improvisação)
    - "Improvisão" and "Improvisação" → same when normalized
    - "Apita o Comboio" and "Apita o Comboio (version 2)" → same base
    - "Oh Nita" parte 1 and "Oh Nita", parte 2 → same base
    """
    if not title1 or not title2:
        return False
    
    def normalize_text(text):
        """Remove accents, quotes, punctuation, trailing numbers/variants, and convert to lowercase"""
        # Remove all types of quotes (regular, smart quotes, etc.)
        text = re.sub(r'["\'""\']', '', text)
        
        # Remove common punctuation (except spaces needed for word separation)
        # Added # to the list of punctuation to remove
        text = re.sub(r'[,\.;:\!\?—–\-#]', ' ', text)
        
        # Decompose accented characters
        nfd = unicodedata.normalize('NFD', text)
        # Remove diacritical marks
        text = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn').lower()
        
        # Remove trailing numbers, parentheses, and common variant markers
        # e.g., "improvisacao 1" → "improvisacao", "video (version 2)" → "video"
        text = re.sub(r'\s*[\(\[].*[\)\]].*$', '', text)  # Remove (variant) or [variant]
        text = re.sub(r'\s+\d+$', '', text)  # Remove trailing arabic numbers with space
        text = re.sub(r'\s+[ivxlcdm]+$', '', text)  # Remove trailing roman numerals (i, ii, iii, iv, v, etc.)
        text = re.sub(r'\s*-\s*\d+$', '', text)  # Remove " - 1" style
        text = re.sub(r'\s*-\s*[ivxlcdm]+$', '', text)  # Remove " - i" style
        text = re.sub(r'\s*v\d+$', '', text)  # Remove " v2" style
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        # Normalize plural forms in Portuguese
        # Handle common Portuguese plural patterns to match singular/plural
        # Examples: modas → moda, lengalengas → lengalenga, canções → cancao
        words = text.split()
        normalized_words = []
        for word in words:
            # Remove trailing 's' for common plural forms (most Portuguese plurals)
            if len(word) > 3 and word.endswith('s'):
                # Common Portuguese plural patterns
                if word.endswith('ões'):  # canções → cancao (need to also handle ã → a)
                    singular = word[:-3] + 'ao'
                elif word.endswith('ães'):  # pães → pao
                    singular = word[:-3] + 'ao'
                elif word.endswith('ais'):  # animais → animal
                    singular = word[:-3] + 'al'
                elif word.endswith('eis'):  # papéis → papel
                    singular = word[:-3] + 'el'
                elif word.endswith('is'):  # barris → barril
                    singular = word[:-2] + 'l'
                elif word.endswith('ns'):  # jardins → jardim
                    singular = word[:-2] + 'm'
                else:
                    # Simple plural: just remove 's'
                    singular = word[:-1]
                normalized_words.append(singular)
            else:
                normalized_words.append(word)
        
        return ' '.join(normalized_words).strip()
    
    title1_normalized = normalize_text(title1.strip())
    title2_normalized = normalize_text(title2.strip())
    
    return title1_normalized == title2_normalized

def filterRelatedTitles(projects, current_project_id):
    """
    Filter out projects with similar titles (series/continuations).
    Keeps the first one in each series.
    """
    if not projects:
        return projects
    
    filtered = []
    seen_base_titles = set()
    
    for project in projects:
        # Skip the current project
        if project.id == current_project_id:
            continue
        
        # Check if this is a related title to any we've already added
        is_related = False
        for filtered_project in filtered:
            if isSimilarTitle(project.title, filtered_project.title):
                is_related = True
                break
        
        if not is_related:
            filtered.append(project)
    
    return filtered

async def buildQueryAndExecute(field, project):

    value = getattr(project, field, None)

    if not value:
        return None, None

    # Build exclusion clause to exclude current project
    exclude_clause = f" AND id != {project.id}"

    # Special handling for date field
    if field == "date":
        try:
            year = value.strftime('%Y-%m-%d').split('-')[0]
            query = f"SELECT * FROM projects WHERE date LIKE '{year}-%'{exclude_clause}"
            #print(f"[Query - date year] {query}")
            results = await asyncio.to_thread(executeQueriesSQL, [query])
            return query, (results[0] if results else None)
        except:
            return None, None

    value_str = str(value)

    # Check if value contains ", "
    if ", " in value_str:
        # Split by ", " and create OR conditions
        elements = [elem.strip() for elem in value_str.split(", ")]
        # Filter out insignificant elements (too short or in ignore list)
        significant_elements = [
            elem for elem in elements 
            if elem and len(elem) > 2 and elem.lower() not in wordsToIgnore
        ]
        if significant_elements:
            conditions = [f"{field} LIKE '%{elem}%'" for elem in significant_elements]
            where_clause = " OR ".join(conditions)
            query = f"SELECT * FROM projects WHERE ({where_clause}){exclude_clause}"
            #print(f"[Query - comma split] {query}")
            results = await asyncio.to_thread(executeQueriesSQL, [query])
            return query, (results[0] if results else None)
        else:
            # Fallback to original exact match if all elements filtered out
            query_exact = f"SELECT * FROM projects WHERE {field} LIKE '%{value_str}%'{exclude_clause}"
            results = await asyncio.to_thread(executeQueriesSQL, [query_exact])
            return query_exact, (results[0] if results else None)
    else:
        # Try exact match first
        query_exact = f"SELECT * FROM projects WHERE {field} LIKE '%{value_str}%'{exclude_clause}"
        #print(f"[Query - exact match] {query_exact}")

        # Execute query to check if it returns results
        results = await asyncio.to_thread(executeQueriesSQL, [query_exact])

        if results and results[0]:  # Has results
            #print(f"[Query - exact match SUCCESS] Found {len(results[0])} results")
            return query_exact, results[0]
        else:
            #print(f"[Query - exact match FAILED] No results, trying word split...")
            # Split by space and filter out insignificant words (short or in ignore list)
            words = [word.strip() for word in value_str.split(" ")]
            coreWords = [
                word for word in words 
                if word and len(word) > 2 and word.lower() not in wordsToIgnore
            ]

            if coreWords:
                conditions = [f"{field} LIKE '%{word}%'" for word in coreWords]
                where_clause = " OR ".join(conditions)
                query = f"SELECT * FROM projects WHERE ({where_clause}){exclude_clause}"
                #print(f"[Query - word split] {query}")
                results = await asyncio.to_thread(executeQueriesSQL, [query])
                return query, (results[0] if results else None)
            else:
                # Fallback to exact match if no significant words (already executed above)
                #print(f"[Query - fallback to exact] {query_exact}")
                return query_exact, (results[0] if results else None)

async def getDirect(project):
    # Pre-filter options to only include fields with data
    validOptions = [opt for opt in directOptions if hasFieldData(opt["field"], project)]

    if not validOptions:
        return []

    # Sort by weight (descending) for better prioritization
    validOptions.sort(key=lambda x: x["p"], reverse=True)

    # Execute queries in parallel for top candidates
    # Try more than nDirect to account for potential empty results
    candidateCount = min(len(validOptions), nDirect * 2)
    candidates = validOptions[:candidateCount]

    # Execute all candidate queries concurrently using asyncio
    tasks = [buildQueryAndExecute(opt["field"], project) for opt in candidates]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)

    # Map successful results
    results_map = {}
    for opt, result in zip(candidates, results_list):
        if isinstance(result, Exception):
            continue
        query, results = result
        if query and results:
            results_map[opt["field"]] = (query, results, opt)

    # Select nDirect results using weighted random from successful queries
    if not results_map:
        return []

    available = list(results_map.values())
    weights = [opt["p"] for _, _, opt in available]

    # Randomly select nDirect items WITHOUT replacement to avoid duplicates
    numToSelect = min(nDirect, len(available))

    # Use custom weighted sampling without replacement
    selected_items = []
    available_copy = available.copy()
    weights_copy = weights.copy()

    for _ in range(numToSelect):
        # Weighted random choice
        selected_idx = random.choices(range(len(available_copy)), weights=weights_copy, k=1)[0]
        selected_items.append(available_copy[selected_idx])

        # Remove selected item to prevent duplicates
        available_copy.pop(selected_idx)
        weights_copy.pop(selected_idx)

    # Build final suggestions with minimal project data
    selected = []
    for query, results, opt in selected_items:
        description = describeDirectSuggestion(query, opt["field"])
        selected.append({
            "description": description,
            "projects": [serializeProjectMinimal(p) for p in results]
        })

    return selected

async def executeDisruptiveQuery(option, project):

    # Pre-check if both fields have data
    if not hasFieldData(option["matchField"], project):
        return None

    # Build and execute match query for the matchField
    match_query, match_results = await buildQueryAndExecute(option["matchField"], project)

    if not match_query:
        return None

    # Get the exclude field value
    exclude_value = getattr(project, option["excludeField"], None)

    if exclude_value:
        # Special handling for date field in exclude
        if option["excludeField"] == "date":
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
                not_conditions = [f"{option['excludeField']} NOT LIKE '%{elem}%'" for elem in elements if elem]
                exclude_condition = " AND " + " AND ".join(not_conditions)
            else:
                # Single value
                exclude_condition = f" AND {option['excludeField']} NOT LIKE '%{exclude_value_str}%'"

        # Combine match query with exclude condition
        final_query = match_query.replace(" AND id !=", exclude_condition + " AND id !=")

        # Execute the disruptive query
        results = await asyncio.to_thread(executeQueriesSQL, [final_query])

        if results and results[0]:
            # Generate dynamic description
            description = describeDisruptiveSuggestion(option["matchField"], option["excludeField"])
            return (option, description, results[0])
    else:
        # No exclude value, use match results (already executed)
        if match_results:
            # Use direct description as fallback
            description = describeDirectSuggestion(match_query, option["matchField"])
            return (option, description, match_results)

    return None

async def getDisruptive(project):
    # Pre-filter options to only include those with valid match fields
    validOptions = [opt for opt in disruptiveOptions if hasFieldData(opt["matchField"], project)]

    if not validOptions:
        return []

    # Randomize order for variety
    random.shuffle(validOptions)

    # Try more candidates in parallel to account for failures
    candidateCount = min(len(validOptions), nDisruptive * 3)
    candidates = validOptions[:candidateCount]

    # Execute all candidate queries concurrently using asyncio
    tasks = [executeDisruptiveQuery(opt, project) for opt in candidates]
    results_list_raw = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out None and exceptions
    results_list = [r for r in results_list_raw if r and not isinstance(r, Exception)]

    # Remove duplicates based on matchField and excludeField combination
    if not results_list:
        return []

    # Create a unique key for each option based on its field combination
    unique_results = {}
    for option, description, projects in results_list:
        key = (option["matchField"], option["excludeField"])
        if key not in unique_results:
            unique_results[key] = (option, description, projects)

    # Convert back to list
    results_list = list(unique_results.values())

    # Randomly select nDisruptive from successful unique results
    numToSelect = min(nDisruptive, len(results_list))
    selected_items = random.sample(results_list, numToSelect)

    # Build final suggestions with minimal project data
    selected = []
    for _, description, projects in selected_items:
        selected.append({
            "description": description,
            "projects": [serializeProjectMinimal(p) for p in projects]
        })

    return selected

def describeSimilarTitles():
    """
    Generate varied descriptions for similar titles suggestions.
    """
    descriptions = [
        "Semelhança no título",
        "Títulos relacionados",
        "Nome parecido",
    ]
    return random.choice(descriptions)

async def getSimilarTitles(project):
    """
    Find projects with similar titles (series/continuations).
    Returns them as a single suggestion block.
    """
    if not project.title:
        return None
    
    # Remove all types of quotes from title before splitting
    title_cleaned = re.sub(r'["\'""\']', '', project.title)
    
    # Extract significant words from title
    # Include Roman numerals (I, II, III, IV, V, VI, VII, VIII, IX, X) and regular numbers
    def is_significant_word(word):
        if len(word) > 2:
            return True
        # Keep Roman numerals (common in Portuguese titles)
        if re.match(r'^[IVXLCDM]+$', word.upper()):
            return True
        # Keep single/double digit numbers
        if word.isdigit():
            return True
        return False
    
    words = [w for w in title_cleaned.split() if is_significant_word(w)]
    
    if not words:
        return None
    
    # Build SQL query with LIKE conditions for each word
    # For each word, search for both the word itself AND its singular/plural variant
    conditions = []
    for word in words:
        # Always add the original word
        conditions.append(f"title LIKE '%{word}%'")
        
        # Add plural/singular variant if word is likely a noun
        word_lower = word.lower()
        if len(word_lower) > 3:
            # If ends in 's', also search for singular (remove 's')
            if word_lower.endswith('s') and len(word_lower) > 4:
                singular = word[:-1]  # Keep original case
                conditions.append(f"title LIKE '%{singular}%'")
            # If doesn't end in 's', also search for plural (add 's')
            elif not word_lower.endswith('s'):
                plural = word + 's'
                conditions.append(f"title LIKE '%{plural}%'")
    
    where_clause = " OR ".join(conditions)
    query = f"SELECT * FROM projects WHERE ({where_clause}) AND id != {project.id}"
    
    results = await asyncio.to_thread(executeQueriesSQL, [query])
    
    if not results or not results[0]:
        return None
    
    # Apply similarity matching only on filtered candidates
    similar_projects = []
    for p in results[0]:
        title = p.title if hasattr(p, 'title') else p.get("title", "")
        if isSimilarTitle(project.title, title):
            similar_projects.append(p)
    
    if not similar_projects:
        return None
    
    return {
        "description": describeSimilarTitles(),
        "projects": [serializeProjectMinimal(p) for p in similar_projects]
    }

# ==================================================
# main
# ==================================================

def getSuggestions(project):

    # Run async functions in sync context
    return asyncio.run(_getSuggestionsAsync(project))

async def _getSuggestionsAsync(project):

    # Get 3 direct, 2 disruptive, and similar titles suggestions concurrently
    direct, disruptive, similar_titles = await asyncio.gather(
        getDirect(project),
        getDisruptive(project),
        getSimilarTitles(project)
    )

    # Combine results - similar titles always first
    result = []
    
    # Add similar titles if found (always first)
    if similar_titles:
        result.append(similar_titles)
    
    # Add direct and disruptive suggestions
    result.extend(direct)
    result.extend(disruptive)

    # Shuffle projects within each suggestion
    for suggestion in result:
        random.shuffle(suggestion["projects"])

    # Shuffle only the direct and disruptive suggestions (keep similar titles first)
    if similar_titles and len(result) > 1:
        # Shuffle everything after the first element
        other_suggestions = result[1:]
        random.shuffle(other_suggestions)
        result = result[:1] + other_suggestions

    return result