class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        # Determine theme
        mode = 'system'
        if request.user.is_authenticated:
            mode = request.user.display_mode
        else:
            mode = request.session.get('display_mode', request.COOKIES.get('display_mode','system'))
        request.display_mode = mode if mode in ('light','dark','system') else 'system'
        response = self.get_response(request)
        # For anonymous, persist via secure cookie if set in session
        if not request.user.is_authenticated and 'display_mode' in request.session:
            response.set_cookie('display_mode', request.session['display_mode'], max_age=60*60*24*365, samesite='Lax', secure=False, httponly=False)
        return response
