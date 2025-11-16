def activate_user(strategy, details, user=None, *args, **kwargs):
    if user:
        user.is_active = True
        user.save()
    return {"user": user}