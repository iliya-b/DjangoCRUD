from .models import User, Pair
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
            password=generate_password(),
        )


def set_field(user_id, key, value):
    user = get_user(user_id)
    setattr(user, key, value)
    user.save()


def create_pair(user_id_a, user_id_b):
    Pair.objects.create(
        user_a=user_id_a,
        user_b=user_id_b,
    )


def delete_pairs():
    Pair.objects.filter().delete()


def get_pairs():
    Pair.objects.all()