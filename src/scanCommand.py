def checkCondition(header, rule):
    if isinstance(rule['condition'], str) and rule['condition'] not in header:
        return True
    elif isinstance(rule['condition'], bool) and rule['condition']:
        return True
    else:
        return False

def clearBadHeaders(intersect, headers, catalog):
    result = dict()
    for header in intersect:
        if isinstance(catalog[header], list):
            for index, rule in enumerate(catalog[header]):
                if checkCondition(headers[header], rule):
                    if header in result:
                        result[header].append(index)
                    else:
                        result[header] = [index]
        else:
            if checkCondition(headers[header], catalog[header]):
                result[header] = True

    return result

def check(headers, catalog, category="good", status=False, headers2analyze=False):
    if isinstance(headers2analyze, list):
        lookFor = headers2analyze
    else:
        lookFor = catalog.keys()

    if category == "good":
        if status:
            result = set(lookFor) & set(headers.keys())
        else:
            result = set(lookFor) - set(headers.keys())
    elif category == "bad":
        result = set(lookFor) & set(headers.keys())
        result = clearBadHeaders(result, headers, catalog)

    return result
