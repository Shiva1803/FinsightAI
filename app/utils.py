import re, unicodedata, difflib

def normalize_name(name):
    if not name:
        return name
    name = unicodedata.normalize('NFKD', name)
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip().lower()

def fuzzy_match(a, b, threshold=0.8):
    if not a or not b:
        return False
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    return ratio >= threshold
