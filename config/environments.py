from dataclasses import dataclass
from enum import Enum
from faker import Faker

fake = Faker()

class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {"dev": "Dev", "stage": "Stage"}[self.value]

@dataclass
class UserCredentials:
    email: str
    password: str
    name: str
    surname: str
    address: str

    @classmethod
    def generate_fake(cls):
        return cls(
            email=fake.email(),
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.last_name(),
            address=fake.address()
        )

common_users = {
    "user": UserCredentials(
        email="ivan1_ivanov1_8@gmail.com", 
        password="123456",
        name="Иван",
        surname="Иванов",
        address="ул. Тестовая, д. 1, кв. 1"
    ),
    "admin": UserCredentials(
        email="vovo_admin@gmail.com", 
        password="123456",
        name="Владимир",
        surname="Администраторов",
        address="ул. Админская, д. 5, кв. 10"
    ),
    "user_order": UserCredentials.generate_fake()
}

@dataclass
class EnvironmentConfig:
    url: str
    default_user: str

    def __str__(self):
        return f"- URL: {self.url}"

environments = {
    Environment.DEV: EnvironmentConfig(
        url="https://qa-scooter.praktikum-services.ru",
        default_user="admin"
    ),
    Environment.STAGE: EnvironmentConfig(
        url="https://qa-mesto.praktikum-services.ru", # Здесь мог бы быть другой URL
        default_user="user"
    )
}

def print_environment_info(env_name, user_type=None):
    """Выводит краткую сводку по тестовому окружению."""
    env = Environment(env_name)
    config = environments[env]
    final_user_type = user_type or config.default_user

    print()
    print(f"Окружение:    {env.value.upper()}")
    print(f"URL:          {config.url}")

    if final_user_type:
        user = common_users.get(final_user_type)
        if user:
            print(f"Пользователь: {user.email}")
    print()