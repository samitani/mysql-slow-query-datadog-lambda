import re

def fingerprint(query):
    query = query.strip().lower()

    query = re.sub(r'\\["\']', '', query)
    query = re.sub(r'[ \n\t\r\f]+', ' ', query)
    query = re.sub(r'\bnull\b', '?', query)
    query = re.sub(r'\b\d+\b', '?', query)

    # "str" => ?
    query = re.sub(r'".*?"', '?', query)
    # 'str' => ?
    query = re.sub(r"'.*?'", '?', query)

    query = re.sub(r'\b(in|values)([\s,]*\([\s?,]*\))+', '\\1(?+)', query)
    query = re.sub(r'\blimit \?(, ?\?| offset \?)?', 'limit ?', query)

    return query
