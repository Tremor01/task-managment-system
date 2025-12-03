from .postgres import BaseRepository
from db.models import User


class UserRepository(BaseRepository[User]):
    MODEL = User

