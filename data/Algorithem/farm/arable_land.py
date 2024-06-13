"""
경작지
:type: 쌓인 작물의 종류
:stack: 쌓인 작물의 갯수
"""

from ..type_repositry import CropType
from ..farm.field import Field
from ..type_repositry import FieldType


class ArableLand(Field):
    def __init__(self):
        self.field_type = FieldType.ARABLE
        self.count = 0
        self.kind = CropType.NONE
