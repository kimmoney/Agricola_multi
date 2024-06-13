from .field import Field
from ..type_repositry import FieldType

'''
집 구상 클래스
'''


class House(Field):
    def __init__(self):
        self.field_type = FieldType.HOUSE
