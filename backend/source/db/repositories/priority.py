from .postgres import BaseRepository
from db.models import Priority


class PriorityRepository(BaseRepository[Priority]):
    MODEL = Priority

