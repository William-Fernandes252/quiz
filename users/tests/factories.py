from factory import Faker  # type: ignore
from factory.django import DjangoModelFactory  # type: ignore

from users import models


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    username = Faker("user_name")
    email = Faker("email")
    password = Faker("password")
    is_staff = False
    is_superuser = False
    is_active = True
