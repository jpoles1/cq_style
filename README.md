# CQ Style - A Neat CadQuery Structure For Your Projects

CadQuery is an open-source Python ecosystem for parametric 3D modeling. It's a great tool for creating customizable and shareable parts. However, there is no clear standard for formatting and organization of projects. CQ Style is here to help! Please read both sections below for our approach to designing parts and keeping your projects organized and accessible.

## How to Organize a CadQuery Project - *The Stylish Way*

Parametric CAD is a wonderful tool for designing your next project. One of its great advantages is the ability to customize and re-use parts, combining them to create sophisticated assemblies which retain their organization and flexibility. Our approach to setting up your development environment should reflect this approach, we want you to be able to create your own parts and use others as well to make your designs come to life. We recommend the following approach to make that possible:

1) Create a root CadQuery projects folder. We recommend you keep all of your CadQuery projects in one place so you can easily import parts from other projects using relative paths.
2) Load `cq_style` into your CadQuery projects folder using the following:
```
mkdir CadQueryDesigns
cd CadQueryDesigns
git clone https://github.com/jpoles1/cq_style.git
```
3) Each project should get its own uniquely named folder; we recommend prefacing all project folder names with `cqs` (Ex: cqs_project/part.py). This indicates to other users that this project is `cq_style` enabled. A project folder can contain as many CadQuery python files as you'd like; we encourage separating each component out into its own file where reasonable, and using a clear naming schema for each file to describe the part it contains.
```
mkdir cqs_project
cd cqs_project
touch part.py
```
6) In order to import `cq_style` from the parent folder you'll using the following:
```
import sys
sys.path.append("../cq_style")
from cq_style import StylishPart
```
6) In order to import a part from another project in the parent folder you'll using the following:
```
import sys
sys.path.append("../cqs_otherproject")

# If your part is contained under the filename "cqs_otherproject.py":
from cqs_otherproject import PartName
p = PartName()

# If your part is contained under any other filename such as "otherpart.py":
from cqs_otherproject import otherpart
p = otherpart.PartName()
# OR you could use:
from cqs_otherproject.otherpart import PartName
p = PartName()
```

7) If using version control, we recommend creating a new git repo for every project rather than using a repo for your entire project directory.

### It's as easy as that, you're now up and running creating your own flexible and nicely organized CadQuery design environment!

## How to Design a CadQuery Part - *The Stylish Way*

As noted above, CadQuery is a great tool for creating customizable, parametric CAD models. It's great to have the ability to make designs parametric, but how do we keep things clean and organized, while exposing the right variables for yourself and other users to customize? This is where `cq_style` comes in!

### What are the advantages to our approach?
- Every part is a class and thus comes with the usual benefits of OOP design: modularity, reusability, flexibility, inheritance, etc.
- The `cq_style` approach means code across the CadQuery community can be more uniform allowing the community to build and innovate together!
- In particular `cq_style` uses the Python ___dataclass__ which makes it easy to specify which variables are intended to be edited by the user (as well as what type the variable should contain). Dataclasses also make writing the code a breeze and cuts down on excessive boilerplate code.
- Within cq_style are a handful of helper functions, which supplement CadQuery's core functionality and help users to hit the ground running with more easily designing their projects.

### Getting started:

If you've followed the above instructions to setup your project directory and download `cq_style` you're all set to get started! We recommend you take a look over `example.py` for a demonstration of how a standard `cq_style` part is written and what each part of the file is used for. You can also jump right in by copying `boilerplate.py` into a file in your new project directory to get things rolling.

# `cq_style` API Overview:
## class StylishPart():

### StylishPart.calc_vars(self):
An "optional" user-defined function which calculates class/self variables which are dependent on the values of params set during instatiation of the class.
Ex: you want to define a dimension as a fraction of a customizable dimension which is input by a user when instantiating the part
```
def calc_vars(self):
    #Example: L is equal to 2x W
    #self.L = 2 * self.W
    return
```

---

### StylishPart.check_config(self):

An "optional" user-defined function which checks over params from instantiation of the class. Should be used to throw warnings/errors if variables are configured incorrectly. 

Note: Runs after calc_vars() on default init so can be used to check calculated variables too_

Ex: You want to make sure that one dimension is always smaller than the other for a customizable part

```
    
    def check_config(self):
        #Example: L should always be greater than H
        #if self.H > self.L:
        #    raise ValueError("Invalid Config: self.H > self.L; height should always be less than length!)") 
        return
```

---

### StylishPart.make(self) -> (Assembly | Workplane):
Main function where final part is assembled. Should return either an Assembly OR Workplane.

Note: It is recommended to avoid calling make() directly on an instantiated StylishPart, instead use part() as below.

---

### StylishPart.part(self, regen: bool = False) -> (Assembly | Workplane)
This function should be used to access the part created by make(). This function caches the part so if it has already been computed during this run you do not need to recompute the design, saving time, especially when working with complex geometries. 
Note: You can regenerate the part rather than using the cached version by setting `regen = True`

---

### StylishPart.display(self, _show_object, regen: bool = False)

Display the part, can be used as part of the function chain (Ex: `StylishPart().export().display(show_object)`) rather than having to wrap with the display function (Ex: `show_object(StylishPart().part()) `).

Note: _show_object can be set to any function that renders a CadQuery part (like `debug()` in CQ Editor or `show()` in Jupyter CadQuery).

### StylishPart.display_split(self, _show_object, regen: bool = False, axis = "XZ", offset: float = 0)

As above, displays the part after splitting it using the provided axis (Ex: "XZ", "YZ", "XY"). You can offset this cutting axis from (0, 0, 0) by setting the offset param. This works with both Workplane and Assembly objects.


### StylishPart.export(self, filepath: str, regen: bool = False)
Exports your part to the specified filepath, identifies export format based on [extension](https://cadquery.readthedocs.io/en/latest/importexport.html) in the filepath (Ex: part.stl, part.step)

### StylishPart.export_split(self, filepath: str, regen: bool = False)
As above, exports the part after splitting it using the provided axis (Ex: "XZ", "YZ", "XY"). You can offset this cutting axis from (0, 0, 0) by setting the offset param. This works with both Workplane and Assembly objects.