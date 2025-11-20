from .postgres import PostgresRepository
from db.models import User


class UserRepository(PostgresRepository[User]):
    MODEL = User

