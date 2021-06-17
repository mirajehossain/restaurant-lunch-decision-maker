import logging
logger = logging.getLogger('django')


def slugify(restaurant_name: str) -> str:
    non_url_safe = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'"]
    non_safe = [c for c in restaurant_name if c in non_url_safe]
    if non_safe:
        for c in non_safe:
            restaurant_name = restaurant_name.replace(c, '')

    slug = '-'.join(restaurant_name.split())
    return slug
