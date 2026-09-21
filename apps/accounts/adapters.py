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
        return ' '.join(part for part in (given, family) if part)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if hasattr(user, 'full_name') and not user.full_name:
            user.full_name = self._name_from_data(data)
        return user

    def pre_social_login(self, request, sociallogin):
        """Populate an empty name on an already-existing Pikestia account."""
        super().pre_social_login(request, sociallogin)

        user = sociallogin.user
        if not hasattr(user, 'full_name') or user.full_name:
            return

        name = self._name_from_data(sociallogin.account.extra_data)
        if name:
            user.full_name = name
            user.save(update_fields=['full_name'])
