from .postgres import BaseRepository
from ..models import Priority


class PriorityRepository(BaseRepository[Priority]):
    MODEL = Priority

