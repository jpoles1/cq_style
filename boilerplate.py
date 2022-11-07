from cadquery import *
from dataclasses import dataclass

import sys
#This should be set to the path of the `cq_style` directory absolute/relative to your project's working directory
cq_style_path = "../cq_style"
sys.path.append(cq_style_path)
from cq_style import StylishPart

@dataclass
class NewPart(StylishPart):
    wall_thickness: float = 1.5

    def check_config(self):
        return

    def calc_vars(self):
        return

    def make(self):
        part = (
            Workplane("XY")
            .box(10,10,10, centered=[1,1,0])
            .faces(">Z").shell(-self.wall_thickness)
        )
        return part

if "show_object" in locals():
    stylish_part = NewPart()
    stylish_part.display(show_object)
    #stylish_part.display_split(show_object)
