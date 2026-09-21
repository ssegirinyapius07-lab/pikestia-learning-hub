from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class PikestiaSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Map trusted Google profile information onto Pikestia's custom User model."""

    @staticmethod
    def _name_from_data(data):
        name = (data.get('name') or '').strip()
        if name:
            return name

        given = (data.get('given_name') or '').strip()
        family = (data.get('family_name') or '').strip()
        return ' '.join(part for part in (given, family) if part).strip()

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if hasattr(user, 'full_name'):
            name = self._name_from_data(data)
            if name:
                user.full_name = name
        return user

    def pre_social_login(self, request, sociallogin):
        """Keep a connected Google profile name synchronized with Pikestia."""
        super().pre_social_login(request, sociallogin)

        if sociallogin.account.provider != 'google':
            return

        name = self._name_from_data(sociallogin.account.extra_data)
        if name and hasattr(sociallogin.user, 'full_name') and sociallogin.user.full_name != name:
            sociallogin.user.full_name = name
            sociallogin.user.save(update_fields=['full_name'])
