from .postgres import PostgresRepository
from db.models import Label


class LabelRepository(PostgresRepository[Label]):
    MODEL = Label

