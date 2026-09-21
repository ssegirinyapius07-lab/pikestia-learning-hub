class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The authenticated user's database preference is authoritative.
        # For anonymous pages, retain the same preference in the session/cookie
        # so login and logout do not cause a visible theme switch.
        if request.user.is_authenticated:
            mode = request.user.display_mode
            request.session['display_mode'] = mode
        else:
            mode = request.session.get(
                'display_mode',
                request.COOKIES.get('display_mode', 'system'),
            )

        request.display_mode = mode if mode in ('light', 'dark', 'system') else 'system'
        response = self.get_response(request)

        # Keep the browser preference aligned on both authenticated and
        # anonymous responses. This survives session cycling and logout.
        response.set_cookie(
            'display_mode',
            request.display_mode,
            max_age=60 * 60 * 24 * 365,
            samesite='Lax',
            secure=False,
            httponly=False,
        )

        return response
