'''
/dataGen/queryFallback.py
-> Multi-level fallback system for handling queries with no results
'''

import re
from database.setup import getConnection

# ==================================================
# Constants
# ==================================================

# Columns to exclude from single-term wildcard search
EXCLUDED_COLUMNS = {'date', 'keywords', 'infoPool', 'id', 'link', 'created_at'}

# All searchable columns in the projects table
SEARCHABLE_COLUMNS = [
    'title', 'author', 'category', 'direction', 'sound',
    'production', 'support', 'assistance', 'research',
    'location', 'instruments'
]

# ==================================================
# Term Extraction Methods
# ==================================================

def extractTermsFromQuery(query):
    """
    Extract search terms wrapped in '% %' from SQL query.
    Also detect if there's a date filter.

    Args:
        query: SQL query string

    Returns:
        dict: {
            'terms': [list of search terms found between % %],
            'dateTerm': str or None (year found in date filter),
            'hasDateFilter': bool
        }
    """
    result = {
        'terms': [],
        'dateTerm': None,
        'hasDateFilter': False
    }

    # Extract all terms between LIKE '%term%'
    # Pattern: LIKE '%something%' or LIKE "%something%"
    termPattern = r"LIKE\s+['\"]%([^%]+?)%['\"]"
    matches = re.findall(termPattern, query, re.IGNORECASE)

    # Check if any term is in a date column
    datePattern = r"date\s+LIKE\s+['\"]%(\d{4})[^'\"]*%['\"]"
    dateMatch = re.search(datePattern, query, re.IGNORECASE)

    if dateMatch:
        result['dateTerm'] = dateMatch.group(1)
        result['hasDateFilter'] = True

    # Collect all non-date terms
    for match in matches:
        term = match.strip()
        # Skip if it's a year (4 digits)
        if term and not re.match(r'^\d{4}$', term):
            if term not in result['terms']:
                result['terms'].append(term)

    return result

def extractTermsFromQueries(queries):
    """
    Extract all unique terms from a list of queries.

    Args:
        queries: List of SQL query strings

    Returns:
        dict: Combined extraction results from all queries
    """
    allTerms = []
    dateTerm = None
    hasDateFilter = False

    for query in queries:
        extracted = extractTermsFromQuery(query)
        allTerms.extend(extracted['terms'])

        if extracted['dateTerm']:
            dateTerm = extracted['dateTerm']
            hasDateFilter = True

    # Remove duplicates while preserving order
    uniqueTerms = []
    for term in allTerms:
        if term not in uniqueTerms:
            uniqueTerms.append(term)

    return {
        'terms': uniqueTerms,
        'dateTerm': dateTerm,
        'hasDateFilter': hasDateFilter
    }

# ==================================================
# Fallback Level Methods
# ==================================================

def buildSingleTermFallback(term, dateFilter=None):
    """
    Level 1 Fallback: Single non-date term found.
    Try every searchable column (except excluded ones) and group results.

    Args:
        term: The single search term to look for
        dateFilter: Optional year/date to filter by

    Returns:
        list: [{
            'query': SQL query string,
            'description': Description for this group,
            'column': Column name being searched
        }]
    """
    queries = []

    for column in SEARCHABLE_COLUMNS:
        baseQuery = f"SELECT * FROM projects WHERE {column} LIKE '%{term}%'"

        # Add date filter if provided
        if dateFilter:
            baseQuery += f" AND date LIKE '%{dateFilter}%'"

        baseQuery += ";"

        # Build description based on column
        columnDescriptions = {
            'title': f"Projetos com '{term}' no título",
            'author': f"Projetos de autores relacionados a '{term}'",
            'category': f"Projetos do género '{term}'",
            'direction': f"Projetos com direção de '{term}'",
            'sound': f"Projetos com som de '{term}'",
            'production': f"Projetos com produção de '{term}'",
            'support': f"Projetos com apoio de '{term}'",
            'assistance': f"Projetos com assistência de '{term}'",
            'research': f"Projetos com pesquisa de '{term}'",
            'location': f"Projetos em localizações relacionadas a '{term}'",
            'instruments': f"Projetos com instrumentos '{term}'"
        }

        queries.append({
            'query': baseQuery,
            'description': columnDescriptions.get(column, f"Projetos com '{term}' em {column}"),
            'column': column
        })

    return queries

def buildKeywordsFallback(term, dateFilter=None):
    """
    Level 2 Fallback: Search in keywords column.

    Args:
        term: The search term
        dateFilter: Optional year/date to filter by

    Returns:
        dict: Single query for keywords search
    """
    query = f"SELECT * FROM projects WHERE keywords LIKE '%{term}%'"

    if dateFilter:
        query += f" AND date LIKE '%{dateFilter}%'"

    query += ";"

    return {
        'query': query,
        'description': f"Outros projetos relacionados a '{term}'",
        'column': 'keywords'
    }

def buildMultiTermFallback(terms, dateFilter=None):
    """
    Level 3 Fallback: Multiple non-date terms found.
    Search keywords column with OR joining all terms.

    Args:
        terms: List of search terms
        dateFilter: Optional year/date to filter by

    Returns:
        dict: Query joining all terms with OR
    """
    # Build OR conditions for all terms
    conditions = [f"keywords LIKE '%{term}%'" for term in terms]
    whereClause = " OR ".join(conditions)

    query = f"SELECT * FROM projects WHERE ({whereClause})"

    if dateFilter:
        query += f" AND date LIKE '%{dateFilter}%'"

    query += ";"

    termsStr = "', '".join(terms)
    return {
        'query': query,
        'description': f"Projetos relacionados a '{termsStr}'",
        'column': 'keywords'
    }

def buildRandomFallback():
    """
    Final Fallback: Return 100 random projects.

    Returns:
        dict: Query for random projects
    """
    return {
        'query': "SELECT * FROM projects ORDER BY RANDOM() LIMIT 100;",
        'description': "Sem potenciais resultados para a sua pesquisa. Continue a Explorar!",
        'column': 'random'
    }

# ==================================================
# Main Fallback Orchestrator
# ==================================================

def applyFallback(originalQueries):
    """
    Apply multi-level fallback based on terms extracted from queries.

    Args:
        originalQueries: List of SQL queries that returned no results

    Returns:
        dict: {
            'queries': [list of fallback queries],
            'descriptions': [list of descriptions],
            'results': [list of result arrays],
            'fallback_level': str
        }
    """
    from database.setup import executeQueriesSQL

    # Extract terms from the original queries
    extracted = extractTermsFromQueries(originalQueries)
    terms = extracted['terms']
    dateFilter = extracted['dateTerm']

    print(f"DEBUG FALLBACK: Extracted terms: {terms}")
    print(f"DEBUG FALLBACK: Date filter: {dateFilter}")

    nonDateCount = len(terms)

    # LEVEL 1: Single non-date term - search all columns
    if nonDateCount == 1:
        term = terms[0]
        print(f"DEBUG FALLBACK: Single term '{term}' - searching all columns")

        fallbackQueries = buildSingleTermFallback(term, dateFilter)

        # Execute and collect results
        allResults = executeQueriesSQL([q['query'] for q in fallbackQueries])

        # Filter out empty results and keep only groups with results
        validGroups = []
        for i, res in enumerate(allResults):
            if res and len(res) > 0:
                validGroups.append({
                    'query': fallbackQueries[i]['query'],
                    'description': fallbackQueries[i]['description'],
                    'results': res
                })

        print(f"DEBUG FALLBACK: Found {len(validGroups)} groups with results")

        # If we have 0 or 1 groups with results, add keywords fallback
        if len(validGroups) <= 1:
            print(f"DEBUG FALLBACK: Adding keywords fallback")
            keywordsQuery = buildKeywordsFallback(term, dateFilter)
            keywordsResults = executeQueriesSQL([keywordsQuery['query']])[0]

            if keywordsResults and len(keywordsResults) > 0:
                validGroups.append({
                    'query': keywordsQuery['query'],
                    'description': keywordsQuery['description'],
                    'results': keywordsResults
                })

        # If still no results, go to final fallback
        if not validGroups:
            print(f"DEBUG FALLBACK: No results found - returning random projects")
            randomQuery = buildRandomFallback()
            randomResults = executeQueriesSQL([randomQuery['query']])[0]

            return {
                'queries': [randomQuery['query']],
                'descriptions': [randomQuery['description']],
                'results': [randomResults],
                'fallback_level': 'random'
            }

        return {
            'queries': [g['query'] for g in validGroups],
            'descriptions': [g['description'] for g in validGroups],
            'results': [g['results'] for g in validGroups],
            'fallback_level': 'single_term_multi_column'
        }

    # LEVEL 2: Multiple non-date terms - search keywords with OR
    elif nonDateCount > 1:
        print(f"DEBUG FALLBACK: Multiple terms {terms} - searching keywords with OR")

        multiTermQuery = buildMultiTermFallback(terms, dateFilter)
        multiTermResults = executeQueriesSQL([multiTermQuery['query']])[0]

        if multiTermResults and len(multiTermResults) > 0:
            return {
                'queries': [multiTermQuery['query']],
                'descriptions': [multiTermQuery['description']],
                'results': [multiTermResults],
                'fallback_level': 'multi_term_keywords'
            }

        # No results - go to final fallback
        print(f"DEBUG FALLBACK: No results found - returning random projects")
        randomQuery = buildRandomFallback()
        randomResults = executeQueriesSQL([randomQuery['query']])[0]

        return {
            'queries': [randomQuery['query']],
            'descriptions': [randomQuery['description']],
            'results': [randomResults],
            'fallback_level': 'random'
        }

    # LEVEL 3: No meaningful terms - return random
    else:
        print(f"DEBUG FALLBACK: No terms found - returning random projects")
        randomQuery = buildRandomFallback()
        randomResults = executeQueriesSQL([randomQuery['query']])[0]

        return {
            'queries': [randomQuery['query']],
            'descriptions': [randomQuery['description']],
            'results': [randomResults],
            'fallback_level': 'random'
        }
