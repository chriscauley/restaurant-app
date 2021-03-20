def get_avatar(backend, user, response, is_new=False, *args, **kwargs):
    if user is None:
        return

    if is_new:
        user.role = 'user'

    if backend.name == 'github':
        user.social_avatar = response['avatar_url']
        user.save()

    if backend.name == 'twitter':
        user.social_avatar = response['profile_image_url']
        user.save()
