from .postgres import PostgresRepository
from db.models import Priority


class PriorityRepository(PostgresRepository[Priority]):
    MODEL = Priority

