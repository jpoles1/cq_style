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

    #Should not be edited
    #If variables need to be calculate on class instantiation, then this should be done under self.calc_vars()
    def __post_init__(self):
        self.calc_vars()

    def calc_vars(self):
        return None

    def make(self):
        #Replace with your own function!
        part = (
            Workplane("XY")
            .box(1,1,1)
        )
        return part

    #Either retrives the cached version of a part, or regenerates it
    def part(self, regen: bool = False):
        if self._stored_part == None or regen:
            self._stored_part = self.make()
        return self._stored_part

    def display(self, _show_object, regen: bool = False):
        _show_object(self.part(regen), name=self.part_name)
        return self
    
    def display_split(self, _show_object, regen: bool = False, axis="XZ"):
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
            _show_object(cross_section, name=self.part_name)
        else:
            _show_object(p.copyWorkplane(Workplane(axis)).split(0,1), name=self.part_name)
        return self

    def export(self, filepath: str, regen: bool = False):
        exporters.export(self.part(regen), filepath)
        return self