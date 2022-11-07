from cadquery import *
from dataclasses import dataclass

import sys
#This should be set to the path of the `cq_style` directory absolute/relative to your project's working directory
cq_style_path = "../cq_style"
sys.path.append(cq_style_path)
from cq_style import StylishPart

@dataclass
class NewPart(StylishPart):
    # This allows the user to set two customizable dimensions, the length and the height
    # We want the length to always be greater than the height and the width to equal 2x the length
    part_W: float = 10
    part_H: float = 8
    wall_thickness: float = 1.5

    # An "optional" user-defined function which checks over params from instantiation of the class
    # Should be used to throw warnings/errors if variables are configured incorrectly
    def check_config(self):
        #Example: We want the length to always be greater than the height
        if self.part_H > self.part_L:
            raise ValueError("Invalid Config: self.H > self.L; height should always be less than length!)") 
        return

    # An "optional" user-defined function which calculates class/self variables which are dependent on the values of params set during instatiation of the class
    # Ex: you want to define a dimension as a fraction of a customizable dimension which is input by a user when instantiating the part
    def calc_vars(self):
        #Example: We want the width to equal 2x the length
        self.part_L = 2 * self.part_W
        return

    def make(self):
        
        a = Assembly()
        
        part = (
            Workplane("XY").box(self.part_L, self.part_W, self.part_H, centered=[1,1,0])
            .faces(">Z").shell(-self.wall_thickness)
            .faces("<Z").circle(self.part_W * 0.2).cutThruAll()
        )

        a.add(part)

        return a

if "show_object" in locals():
    p1 = NewPart().display(show_object)
    #Customize parameters of the part on creation of a new part instance
    NewPart(part_H = p1.part_H * 1.5).display_split(lambda p, name: show_object(p.translate(Vector(p1.part_L * 1.25, 0, 0))), axis="XZ")
    # Get creative and you can find many ways to display different aspects of your part
    # The display_split() function will cut parts (including assemblies) in half along an axis
    # to show features that might otherwise be difficult to visualize
    NewPart().display_split(lambda p, name: show_object(p.translate(Vector(0, 0, p1.part_H * 1.5))), axis="YZ")
