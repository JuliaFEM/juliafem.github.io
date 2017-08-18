---
title: Natural Frequency Calculation Example

author: Marja Rapo
---

### The model

The example model is a bracket that is attached to two adapter plates via tie contacts. The adapter plates are constrained from one of their side as fixed.

![Alt text](https://user-images.githubusercontent.com/28561253/29460847-205aff2c-8432-11e7-8a8b-0505f3c4ff3d.PNG)

The Bracket is modeled as cast iron while the Adapter plates are modeled as steel.

The material parameters are listed in the following table.

| Part           | Material  | E [MPa] | μ     | ρ [kg/m<sup>3</sup>] |
| -------------- |:---------:| -------:|------:|---------------------:|
| Adapter plates | Steel     | 208000  | 0.30  | 7800                 |
| LDU Bracket    | Cast Iron | 165000  | 0.275 | 7100                 |

### The code

First all the packages needed in the calculation are included by typing `using package_name `.

```julia
using JuliaFEM
using JuliaFEM.Preprocess
using JuliaFEM.Postprocess
using JuliaFEM.Abaqus: create_surface_elements
```

The mesh needs to be read from ABAQUS input file to JuliaFEM. The function `abaqus_read_mesh(ABAQUS_input_file_name::String)` will do the trick.

```julia
# read mesh
mesh = abaqus_read_mesh("LDU_ld_r2.inp")
```

`Problem(problem_type, problem_name::String, problem_dimension)` function will construct a new field problem where `problem_type` is the type of the problem (Elasticity, Dirichlet, Mortar etc.), `problem_name::String` is the name of the problem and `problem_dimension` is the number of DOF:s in one node (1 in a heat problem, 2 in a 2D problem, 3 in an elastic 3D problem, 6 in a 3D beam problem, etc.).

`create_elements(mesh, Element_set_name::String)` function will collect the element sets from the ABAQUS input file. In this example the element sets are named as `bracket_elements` and `adapterplate_elements`.

`update!(element_set_name, parameter::String, value)` will update the material parameters for the model. In this example there are two different materials for the two different element sets.

The element sets are then added into the element list of the Problem: `add_elements!(bracket, bracket_elements)`, `add_elements!(bracket, adapterplate_elements)`

```julia
# create a field problem with two different materials
bracket = Problem(Elasticity, "LDU_Bracket", 3)
bracket_elements = create_elements(mesh, "LDUBracket")
adapterplate_elements = create_elements(mesh, "Adapterplate1", "Adapterplate2")
update!(bracket_elements, "youngs modulus", 208.0E3)
update!(bracket_elements, "poissons ratio", 0.30)
update!(bracket_elements, "density", 7.80E-9)
update!(adapterplate_elements, "youngs modulus", 165.0E3)
update!(adapterplate_elements, "poissons ratio", 0.275)
update!(adapterplate_elements, "density", 7.10E-9)
add_elements!(bracket, bracket_elements)
add_elements!(bracket, adapterplate_elements)
```

Boundary conditions can be created from node sets. `Problem(problem_type, problem_name::String, problem_dimension, parent_field_name::String)` function is used again to perform this. In this method the problem type is Dirichlet and `parent_field_name` is the type of the Dirichlet variable ("temperature", "displacement", etc.).

Then the fixed nodal elements are collected from the input file with the function `create_nodal_elements(mesh::Mesh, node_set_name::String)`.

The displacements are then updated with `update!(node_set_name::String, parent_field_name direction::String, value)` where `direction` is the direction of the displacement and `value` is the value of the nodal displacement which of course is 0.0 since our elements are fixed.

```julia
# create a boundary condition from a node set
fixed = Problem(Dirichlet, "fixed", 3, "displacement")
fixed_elements = create_nodal_elements(mesh, "Face_constraint_1")
update!(fixed_elements, "displacement 1", 0.0)
update!(fixed_elements, "displacement 2", 0.0)
```

JuliaFEM allows new functions to be built with the help of other JuliaFEM functions. For example we need now a helper function to create tie contacts to our model. 

Our function is called `create_interface` and it has three variables: mesh, slave and master. `mesh` refers to our input file name that is defined at the begining of this document, `slave` is the name of our slave surface in the input file and `master` is the name of the master surface. The function uses `Problem()` function with the `Mortar` method, `create_surface_elements` function and `update!` function from the JuliaFEM library.

```julia
""" A helper function to create tie contacts. """
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

Interfaces can now be applied with our own function `create_interface(mesh, slave::String, master::String)` that collects necessary information from our input file and creates a tie contact.

```julia  
# call the helper function to create tie contacts
tie1 = create_interface(mesh,
	"LDUBracketToAdapterplate1",
    "Adapterplate1ToLDUBracket") 
tie2 = create_interface(mesh,
	"LDUBracketToAdapterplate2",
    "Adapterplate2ToLDUBracket")
```  

All problems need to be added into `Solver(solver_type, problem_names)` function where `solver_type` is the type of the solver (Modal, Linear, Nonlinear). In this example we are using a modal solver that solves generalized eigenvalue problems Ku = Muλ since we are calculating natural frequencies.

The results can be imported to xdmf file format for further review. This is performed by typing `solver_name.xdmf = Xdmf(result_file_name::String)` where `solver_name` is the name of our solver which we defined and `result_file_name` is the name we want to give our xdmf result file.

Yet we need to specify some properties for our analysis. We only want to calculate the first six frequencies for our model. This can be done by first typing `solver_name.properties.nev = value` where `nev` refers to the number of eigenmodes and `value` is the number of eigenmodes which are to be calculated, and then typing `bracket_freqs.properties.which = :SM` where `which` refers to the type of the eigenmodes (:SM, :LM , etc.) and `:SM` specifies that the eigen modes to be calculated shall be the smallest ones.

Finally by simply typing `solver_name()` we are commanding JuliaFEM to start the analysis.

```julia
# add the field and the boundary problems to the solver
bracket_freqs = Solver(Modal, bracket, fixed, tie1, tie2)
# save results to Xdmf data format ready for ParaView visualization
bracket_freqs.xdmf = Xdmf("results")
# solve 6 smallest eigenvalues
bracket_freqs.properties.nev = 6
bracket_freqs.properties.which = :SM
bracket_freqs()
```

### Results

JuliaFEM gives the following calculation results for the analysis.

| Mode | f [Hz] |
| ---- |:------:|
| 1    | 111.38 |
| 2    | 155.03 |
| 3    | 215.40 |
| 4    | 358.76 |
| 5    | 409.65 |
| 6    | 603.51 |
