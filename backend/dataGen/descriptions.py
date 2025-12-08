'''
/dataGen/descriptions.py
-> generate human-friendly Portuguese descriptions for the suggestions
'''

import random

# ==================================================
# methods
# ==================================================

def describeDirectSuggestion(query, field=None):
    if "where" not in query.lower():
        return "Todos os vídeos da MPAGDP"

    templates_map = {
        "author": ["Mesmo autor", "Do mesmo criador", "Mesma autoria", "Semelhança no autor", "Mais deste autor"],
        "category": ["Mesma categoria", "Categoria semelhante", "Mesmo género de projeto", "Tipo de projeto similar"],
        "location": ["Mesmo local", "Mesmo lugar", "Geografia próxima", "Aconteceu por perto", "Mais neste sítio"],
        "date": ["Mesmo ano", "Época similar", "Pela mesma altura"],
        "instruments": ["Mesmos instrumentos", "Sons parecidos", "Instrumentos em comum", "Timbre aproximado"],
        "keywords": ["Temas semelhantes", "Assuntos parecidos", "Temáticas próximas", "Conceitos parecidos"],
        "title": ["Título semelhante", "Título parecido", "Título relacionado", "Títulos próximos"],
        "direction": ["Mesma realização", "Realização semelhante", "Mesmo realizador"],
        "sound": ["Mesmo engenheiro de som", "Técnico de som em comum"],
        "production": ["Mesma produção", "Mesmo produtor", "Produtor em comum"],
        "support": ["Mesmo apoio", "Apoios em comum", "Mesmos apoiantes"],
        "assistance": ["Mesma assistência", "Assistentes em comum"],
        "research": ["Mesmos investigadores", "Pesquisadores em comum"]
    }

    if field in templates_map:
        return random.choice(templates_map[field])

    return random.choice(["Vídeos relacionados", "Conteúdo semelhante", "Trabalhos parecidos", "Projetos similares"])

def describeDisruptiveSuggestion(matchField, excludeField):
    fieldData = {
        "author": [
            {"term": "autor", "gender": "m", "number": "s"},
            {"term": "criador", "gender": "m", "number": "s"}
        ],
        "category": [
            {"term": "categoria", "gender": "f", "number": "s"},
            {"term": "género", "gender": "m", "number": "s"},
            {"term": "tipo", "gender": "m", "number": "s"}
        ],
        "location": [
            {"term": "local", "gender": "m", "number": "s"},
            {"term": "localização", "gender": "f", "number": "s"},
            {"term": "lugar", "gender": "m", "number": "s"},
            {"term": "sítio", "gender": "m", "number": "s"}
        ],
        "date": [
            {"term": "altura", "gender": "f", "number": "s"},
            {"term": "ano", "gender": "m", "number": "s"},
            {"term": "época", "gender": "f", "number": "s"}
        ],
        "instruments": [
            {"term": "instrumentos", "gender": "m", "number": "p"},
            {"term": "sonoridade", "gender": "f", "number": "s"}
        ]
    }

    matchOptions = fieldData.get(matchField, [{"term": matchField, "gender": "m", "number": "s"}])
    excludeOptions = fieldData.get(excludeField, [{"term": excludeField, "gender": "m", "number": "s"}])

    matchData = random.choice(matchOptions)
    excludeData = random.choice(excludeOptions)

    matchName = matchData["term"]
    excludeName = excludeData["term"]

    if matchData["number"] == "p":
        matchMesmo = "mesmas" if matchData["gender"] == "f" else "mesmos"
        matchProximo = "próximas" if matchData["gender"] == "f" else "próximos"
        matchSemelhante = "semelhantes"
    else:
        matchMesmo = "mesma" if matchData["gender"] == "f" else "mesmo"
        matchProximo = "próxima" if matchData["gender"] == "f" else "próximo"
        matchSemelhante = "semelhante"

    if excludeData["number"] == "p":
        excludeOutro = "outras" if excludeData["gender"] == "f" else "outros"
        excludeDistinto = "distintas" if excludeData["gender"] == "f" else "distintos"
        excludeDiferente = "diferentes" 
    else:
        excludeOutro = "outra" if excludeData["gender"] == "f" else "outro"
        excludeDistinto = "distinta" if excludeData["gender"] == "f" else "distinto"
        excludeDiferente = "diferente"


    templates = [
        f"{excludeOutro.capitalize()} {excludeName}, {matchMesmo} {matchName}",
        f"{excludeName.capitalize()} {excludeDiferente}, {matchName} {matchProximo}",
        f"{excludeName.capitalize()} {excludeDiferente}, {matchName} {matchSemelhante}",
        f"{matchMesmo.capitalize()} {matchName}, {excludeName} {excludeDiferente}",
        f"{matchMesmo.capitalize()} {matchName}, {excludeName} {excludeDistinto}",
        f"{excludeName.capitalize()} {excludeDistinto}, {matchName} {matchSemelhante}",
        f"{excludeOutro.capitalize()} {excludeName}, {matchName} {matchProximo}",
        f"{excludeOutro.capitalize()} {excludeName}, {matchName} {matchSemelhante}",
        f"{matchName.capitalize()} {matchProximo}, {excludeName} {excludeDiferente}",
        f"{matchName.capitalize()} {matchSemelhante}, {excludeName} {excludeDiferente}",
        f"{matchName.capitalize()} {matchProximo}, {excludeOutro} {excludeName}",
        f"{matchName.capitalize()} {matchSemelhante}, {excludeOutro} {excludeName}",
    ]

    return random.choice(templates)