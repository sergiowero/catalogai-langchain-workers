def dict_distinct(dict1, dict2):
    """
    Compare two dictionaries for distinct values.
    Returns True if they are distinct, False otherwise.
    """

    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict1 != dict2
    for key in dict1:
        if key not in dict2 or dict_distinct(dict1[key], dict2[key]):
            return True
    for key in dict2:
        if key not in dict1 or dict_distinct(dict1[key], dict2[key]):
            return True
    return False
