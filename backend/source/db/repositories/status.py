from .postgres import BaseRepository
from db.models import Status


class StatusRepository(BaseRepository[Status]):
    MODEL = Status

