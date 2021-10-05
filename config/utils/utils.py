from math import ceil


def paginated_response(queryset, *, per_page=10, page=1):
    try:
        total_count = len(queryset)
    except TypeError:
        total_count = 1
    limit = per_page
    offset = per_page * (page - 1)
    page_count = ceil(total_count / per_page)

    try:
        data = list(queryset[offset: limit + offset])
    except TypeError:
        data = queryset

    return {
        'total_count': total_count,
        'per_page': limit,
        'from_record': offset + 1,
        'to_record': (offset + limit) if (offset + limit) <= total_count else (total_count % per_page) + offset,
        'previous_page': page - 1 if page > 2 else 1,
        'current_page': page,
        'next_page': min(page + 1, page_count),
        'page_count': page_count,
        'data': data,
    }


def response(status, data, *, paginated: bool = False, per_page: int = 10, page: int = 1):
    if paginated:
        return status, paginated_response(data, per_page=per_page, page=page)

    return status, data
