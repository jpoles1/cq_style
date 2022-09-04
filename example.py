from cadquery import *
from dataclasses import dataclass

import sys
sys.path.append("../cq_style")
from cq_style import StylishPart

@dataclass
class NewPart(StylishPart):
    part_param: float = 1234
    def make(self):
        part = cq.Workplane("XY").sphere(1)
        return part