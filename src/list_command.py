def list_headers(catalog, headers=True):
    result = []
    if isinstance(headers, set):
        for header in catalog:
            if header in headers:
                result.append(header)
    else:
        result = catalog.keys()

    return set(result)
