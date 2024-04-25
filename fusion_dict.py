def fusionner_dictionnaires(d1, d2):
    # Si l'un des dictionnaires est vide, retourner l'autre
    if not d1:
        return d2
    if not d2:
        return d1
    
    # Fusionner les clés de d2 dans d1
    for cle, valeur in d2.items():
        if cle in d1:
            # Si la valeur est un dictionnaire, fusionner récursivement
            if isinstance(valeur, dict) and isinstance(d1[cle], dict):
                d1[cle] = fusionner_dictionnaires(d1[cle], valeur)
            else:
                d1[cle] = valeur
        else:
            d1[cle] = valeur
    
    return d1
