from django.utils.timezone import now

from .models import Team, User, Pair
from .utils import generate_password


def get_user(user_id):
    return User.objects.filter(telegram_id=user_id).first()


def get_admins():
    return User.admins.all()


def get_users():
    User.objects.all()


def get_active_users():
    return User.objects.filter(is_active=True).all()


def create_user(user_id):
    if not get_user(user_id):
        User.objects.create(
            telegram_id=user_id,
            created_at=now()
        )
    return get_user(user_id)


def set_field(object, key, value):
    setattr(object, key, value)
    object.save()


def create_pair(user_id_a, user_id_b):
    Pair.objects.create(
        user_a=user_id_a,
        user_b=user_id_b,
    )


def delete_pairs():
    Pair.objects.filter().delete()


def get_pairs():
    Pair.objects.all()


def get_team(name):
    return Team.objects.filter(name=name).first()


def get_team_by_password(password):
    return Team.objects.filter(password=password).first()


def create_team(name, user):
    if not get_team(name):
        Team.objects.create(
            name=name,
            password=generate_password(),
            admin=user
        )
    return get_team(name)
