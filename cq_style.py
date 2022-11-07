from dataclasses import dataclass, asdict
from cadquery import Assembly, Workplane, exporters

#Import me into your CadQuery projects by adding the lines below:
'''
from dataclasses import dataclass
import sys
sys.path.append("../cq_style")
from cq_style import StylishPart
'''

#Define a new part with:
'''
@dataclass
class NewPart(StylishPart):
    part_param: float = 1234
    def make(self):
        part = ...
        return part
'''

#At end of new StylishPart class definition files you can include the following to render the given file when it is opened in CQ-Editor
#Below you see the show_object() function passed to the display or display_split functions. This is for CQ-Editor and can be replaced with show(), debug(), etc.
'''
if "show_object" in locals():
    StylishPart().display(show_object)
    StylishPart().display_split(show_object)
'''

@dataclass
class StylishPart:
    part_name = None
    _stored_part = None

    #This class method lets you create instances of child classes from the base class!
    @classmethod
    def from_instance(cls, instance):
        #Remove keys which should not be overridden on instance of child class
        dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i not in set(y)])
        return cls(**dictfilt(asdict(instance), ["floor_h", "lip_h"]))

    # DO NOT EDIT/OVERWRITE!
    # IF you do, you should make sure to include: self.check_config(); self.calc_vars();
    #
    # If variables need to be checked for errors on class instantiation, use self.check_config()
    # If variables need to be calculated on class instantiation, use self.calc_vars()
    def __post_init__(self):
        self.calc_vars()
        self.check_config()

    # An "optional" user-defined function which calculates class/self variables which are dependent on the values of params set during instatiation of the class
    # Ex: you want to define a dimension as a fraction of a customizable dimension which is input by a user when instantiating the part
    def calc_vars(self):
        #Example: L is equal to 2x W
        #self.L = 2 * self.W
        return


    # An "optional" user-defined function which checks over params from instantiation of the class
    # Should be used to throw warnings/errors if variables are configured incorrectly
    # Runs after calc_vars() on default init so can be used to check calculated variables too
    # Ex: You want to make sure that one dimension is always smaller than the other for a customizable part...
    def check_config(self):
        #Example: L should always be greater than H
        #if self.H > self.L:
        #    raise ValueError("Invalid Config: self.H > self.L; height should always be less than length!)") 
        return

    def make(self):
        #Replace with your own function!
        part = (
            Workplane("XY")
            .box(1,1,1)
        )
        return part

    # Either retrives the cached version of a part, or regenerates it
    def part(self, regen: bool = False):
        if self._stored_part == None or regen:
            self._stored_part = self.make()
        return self._stored_part

    # Display the object using _show_object()
    # Ex: if using CQ Editor: [show_object, debug, ...]
    # Ex: if using Jupyter CadQuery: [show, ...]
    def display(self, _show_object, regen: bool = False):
        _show_object(self.part(regen), name=self.part_name)
        return self
    
    # Splits object in half along the provided axis (eg: ["XZ", "YZ", "XY"]) or Plane and then displays
    def display_split(self, _show_object, regen: bool = False, axis="XZ", offset=0):
        p = self.part(regen)
        if isinstance(p, Assembly):
            #Allows for splitting of Assembly while maintaining colors
            cross_section = Assembly(None, name=p.name)
            for name, subpart in p.traverse():
                location = p.findLocation(name)
                for shape in subpart.shapes:
                    cross_section.add(
                        Workplane("XY").add(shape.located(location)).copyWorkplane(Workplane(axis).workplane(offset=offset)).split(0,1),
                        color=subpart.color,
                        name=name,
                    )
            _show_object(cross_section, name=self.part_name)
        else:
            _show_object(p.copyWorkplane(Workplane(axis)).split(0,1), name=self.part_name)
        return self

    # Exports model (shape or assembly) to file
    def export(self, filepath: str, regen: bool = False):
        p = self.part(regen)
        if isinstance(p, Assembly):
            p.save(filepath)
        else:
            exporters.export(p, filepath)
        return self

    # Splits model (shape or assembly) in half along the provided axis (eg: ["XZ", "YZ", "XY"]) or Plane and then exports
    def export_split(self, filepath: str, regen: bool = False, axis="XZ"):
        p = self.part(regen)
        if isinstance(p, Assembly):
            #Allows for splitting of Assembly while maintaining colors
            cross_section = Assembly(None, name=p.name)
            for name, subpart in p.traverse():
                location = p.findLocation(name)
                for shape in subpart.shapes:
                    cross_section.add(
                        Workplane("XY").add(shape.located(location)).copyWorkplane(Workplane(axis)).split(0,1),
                        color=subpart.color,
                        name=name,
                    )
            cross_section.save(filepath)
        else:
            exporters.export(p.copyWorkplane(Workplane(axis)).split(0,1), filepath)
        return self
