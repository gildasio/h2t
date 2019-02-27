def listHeaders(catalog, headers=True):
    result = []
    if isinstance(headers, list):
        for header in catalog:
            if header in headers:
                result.append(header)
    else:
        result = catalog.keys()

    return set(result)
