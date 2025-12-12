from .postgres import BaseRepository
from ..models import Label


class LabelRepository(BaseRepository[Label]):
    MODEL = Label

