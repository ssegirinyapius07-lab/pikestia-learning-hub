import bleach


ALLOWED_CONTENT_TAGS = [
    'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'em',
    'code', 'pre', 'blockquote', 'a', 'table', 'thead', 'tbody',
    'tr', 'th', 'td', 'br', 'hr',
]
ALLOWED_CONTENT_ATTRS = {
    'a': ['href', 'title', 'rel'],
}
ALLOWED_CONTENT_PROTOCOLS = {'http', 'https', 'mailto'}


def sanitize_content(value):
    return bleach.clean(
        value or '',
        tags=ALLOWED_CONTENT_TAGS,
        attributes=ALLOWED_CONTENT_ATTRS,
        protocols=ALLOWED_CONTENT_PROTOCOLS,
        strip=True,
        strip_comments=True,
    )
