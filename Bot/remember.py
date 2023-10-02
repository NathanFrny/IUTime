from enum import Enum


class Remember(Enum):
    ONEDAY = 1
    TREEDAY = 3
    ONEWEEK = 7
    ALWAYS = 310  # Number of day between french school year's start and it's end
