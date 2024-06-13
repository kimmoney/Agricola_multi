from abc import ABC, abstractmethod
from ..type_repositry import FieldType

'''
필드 한칸의 인터페이스
'''


class Field(ABC):
    field_type = FieldType.NONE_FIELD
    kind = None
    count = None
    barn = False
    maximum = 0
