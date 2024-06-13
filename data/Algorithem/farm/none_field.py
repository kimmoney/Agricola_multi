"""
null값의 역할을 수행하는 noneField
"""
from ..type_repositry import AnimalType
from .field import Field
from ..type_repositry import FieldType


class NoneField(Field):
    def __init__(self):
        self.field_type = FieldType.CAGE
        self.kind = None
        self.count = 0
        self.maximum = 0
        self.barn = False
