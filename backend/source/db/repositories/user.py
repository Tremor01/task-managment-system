from .postgres import BaseRepository
from ..models import User


class UserRepository(BaseRepository[User]):
    MODEL = User

