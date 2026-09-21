def theme_and_cookies(request):
    return {
        'display_mode': getattr(request, 'display_mode', 'system'),
        'cookie_consent': request.COOKIES.get('cookie_consent', None),
    }
