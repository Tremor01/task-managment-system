from .postgres import PostgresRepository
from db.models import Status


class StatusRepository(PostgresRepository[Status]):
    MODEL = Status

