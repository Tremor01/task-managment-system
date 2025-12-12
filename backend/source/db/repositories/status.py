from .postgres import BaseRepository
from ..models import Status


class StatusRepository(BaseRepository[Status]):
    MODEL = Status

