---
title: Natural Frequency Calculation Example

author: Marja Rapo
---


First type ```using 'package_name' ``` for all the packages needed in the calculation.

```julia
using JuliaFEM
using JuliaFEM.Preprocess
using JuliaFEM.Postprocess
using JuliaFEM.Abaqus: create_surface_elements
```

The mesh needs to be read from ABAQUS to JuliaFEM. The function ```abaqus_read_mesh('ABAQUS_input_file_name'::String)``` will do the trick.
```info()``` will give information about the element and surface sets in the model.

```julia
mesh = abaqus_read_mesh("LDU_ld_r2.inp")
info("element sets = ", collect(keys(mesh.element_sets)))
info("surface sets = ", collect(keys(mesh.surface_sets)))
```

```Problem('problem_type', 'problem_name'::String, 'problem_dimension')``` function will construct a new field problem where ```'problem_type'``` is the type of the problem (Elasticity, Dirichlet, etc.), ```'problem_name'::String``` is the name of the problem and ```'problem_dimension'``` is the number of DOF:s in one node (1 in a heat problem, 2 in a 2D problem, 3 in an elastic 3D problem, 6 in a 3D beam problem, etc.).

```create_elements(mesh, 'Element_set_name_from_the_.inp_file'::String)``` function will collect and rename the element sets of the model mesh. In this example the element sets are renamed as ```els1``` and ```els2```.

```update!('element_set_name', 'parameter'::String, 'value')``` will update the material parameters for the model. In this example there are two different materials for the two different element sets.

The element sets are then pulled together into an array that is named ```bracket.elements```.

```julia
bracket = Problem(Elasticity, "LDU_Bracket", 3)
els1 = create_elements(mesh, "LDUBracket")
els2 = create_elements(mesh, "Adapterplate1", "Adapterplate2")
update!(els1, "youngs modulus", 208.0E3)
update!(els1, "poissons ratio", 0.30)
update!(els1, "density", 7.80E-9)
update!(els2, "youngs modulus", 165.0E3)
update!(els2, "poissons ratio", 0.275)
update!(els2, "density", 7.10E-9)
bracket.elements = [els1; els2]
```

The boundary conditions need to be created from the node sets. The ```Problem()``` function is used again to perform this.

Then the fixed nodes and the fixed elements of the model are defined.

The displacements are then updated to the solver with the ```update!('fixed_elements_name')```

```julia
fixed = Problem(Dirichlet, "fixed", 3, "displacement")
fixed_nodes = mesh.node_sets[:Face_Constraint_1]
fixed.elements = [Element(Poi1, [nid]) for nid in fixed_nodes]
update!(fixed.elements, "displacement 1", 0.0)
update!(fixed.elements, "displacement 2", 0.0)
```


```julia
function create_interface(mesh::Mesh, slave::String, master::String)
    interface = Problem(Mortar, "tie contact", 3, "displacement")
    interface.properties.dual_basis = false
    slave_elements = create_surface_elements(mesh, slave)
    master_elements = create_surface_elements(mesh, master)
    nslaves = length(slave_elements)
    nmasters = length(master_elements)
    update!(slave_elements, "master elements", master_elements)
    interface.elements = [slave_elements; master_elements]
    return interface
  end
```

update!(fixed.elements, "displacement 3", 0.0)
```
