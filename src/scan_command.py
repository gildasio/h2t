import re


def check_condition(header, rule):
    if isinstance(rule['condition'], str) and re.search(rule['condition'], header):
        return True
    elif isinstance(rule['condition'], bool) and rule['condition']:
        return True
    else:
        return False


def clear_bad_headers(intersect, headers, catalog):
    result = dict()
    for header in intersect:
        if isinstance(catalog[header], list):
            for index, rule in enumerate(catalog[header]):
                if check_condition(headers[header], rule):
                    if header in result:
                        result[header].append(index)
                    else:
                        result[header] = [index]
        else:
            if check_condition(headers[header], catalog[header]):
                result[header] = True

    return result


def check(headers, catalog, category='good', status=False, headers_to_analyze=False):
    if isinstance(headers_to_analyze, set):
        lookFor = headers_to_analyze
    else:
        lookFor = catalog.keys()

    if category == 'good':
        if status:
            result = set(lookFor) & set(headers.keys())
        else:
            result = set(lookFor) - set(headers.keys())
    elif category == 'bad':
        result = set(lookFor) & set(headers.keys())
        result = clear_bad_headers(result, headers, catalog)

    return result


def ignore_headers(result, ignore):
    if not isinstance(ignore, list):
        return result
    elif isinstance(result, set):
        return result - set(ignore)
    elif isinstance(result, dict):
        for i in result:
            if i in ignore:
                del result[i]
        return result
