from .postgres import BaseRepository
from db.models import Label


class LabelRepository(BaseRepository[Label]):
    MODEL = Label

