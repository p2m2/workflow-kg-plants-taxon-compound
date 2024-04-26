def merge_dictionaries(d1, d2):
    # If either dictionary is empty, return the other
    if not d1:
        return d2
    if not d2:
        return d1
    
    # Merge keys from d2 into d1
    for key, value in d2.items():
        if key in d1:
            # If the value is a dictionary, merge recursively
            if isinstance(value, dict) and isinstance(d1[key], dict):
                d1[key] = merge_dictionaries(d1[key], value)
            else:
                d1[key] = value
        else:
            d1[key] = value
    
    return d1
