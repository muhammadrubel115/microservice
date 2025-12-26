from core.models import Profile

def get_or_create_profile(user_uuid):
    profile, _ = Profile.objects.get_or_create(user_uuid=user_uuid)
    return profile
