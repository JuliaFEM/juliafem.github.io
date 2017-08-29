---
layout: example
title: Reordering nodes with the Reverse Cuthill-McKee algorithm
author: Marja Rapo
date: 2017-08-29 17:30:00 +0300
categories: RCM juliafem-0.3.3
---

The analysis is performed with JuliaFEM v0.3.3.

# Introduction

"In numerical linear algebra, the Cuthill–McKee algorithm (CM), named for Elizabeth 
Cuthill and James McKee, is an algorithm to permute a sparse matrix that has 
a symmetric sparsity pattern into a band matrix form with a small bandwidth. The 
reverse Cuthill–McKee algorithm (RCM) due to Alan George is the same algorithm but 
with the resulting index numbers reversed. In practice this generally results 
in less fill-in than the CM ordering when Gaussian elimination is applied." 
(Wikipedia: Cuthill–McKee algorithm)

Basically the algorithm reduces bandwidth of a matrix by reordering nodes in a mesh 
(or vertices in a graph) in the degree order. 

# The mesh

The figure below shows the original mesh in the example. The mesh has 9 elements 
and 15 nodes. Two of the elements are type Tri3 and the rest of the elements’ types 
are Quad4.

<img src="{{ site.url }}/assets/2017-08-29-reordering-nodes-with-the-RCM-algorithm/mesh.PNG">

# Theory

The degree is the number of nodes one node is adjacent to. The degree ordering 
begins from the starting node (the lowest degree node), let us call it P and in tour 
example P = 15 with the degree of 2. Then all nodes adjacent to P in their degree 
order (lowest degree first), which are nodes 1 and 4, are added. Now nodes 1 and 4 
both have the same degree, which is 3, so their order don't matter. We decide to add 
1 first, then 4. Now since 1 was first we will first focus on nodes adjacent to 1 
which are the nodes 15, 3 and 8. Since we already have 15 in our new order list, we 
skip it. The degree of node nr. 3 is 3 and the degree of node nr. 8 is 4. So again 
we are ordering the nodes in the increasing degree order: 3 comes first, then 8. Now 
we will go back to node nr. 4. Node 4 is adjacent to nodes 15, 8 and 10. 15 and 8 
are already ordered so 10 will be the next in the order. Now we go back to node 
number 3 and order its adjacencies. We will continue the ordering until we have 
ordered all nodes in the mesh. The final order is
 `[15, 1, 4, 3, 8, 10, 11, 2, 5, 13, 7, 12, 6, 9, 14]`. 
This is called the Cuthill-McKee order. Since we want the Reverse Cuthill-McKee order 
we simply reverse the order and we get the final order to be 
`[14, 9, 6, 12, 7, 13, 5, 2, 11, 10, 8, 3, 4, 1, 15]`.

### The code

First we include all the packages needed in our calculation. PyPlot is used only to 
visualize the matrices in this example.

```Julia
using NodeNumbering: create_adjacency_graph, node_degrees, RCM, renumbering, 
create_RCM_adjacency, adjacency_visualization
using PyPlot: matshow
```

Then we need to list our elements and their nodes in the mesh. We also need to choose 
the starting node P which should be a node with the lowest degree. We import two Dicts 
into our code and define P:

```julia
elements = Dict(
                  1 => [15, 1, 8, 4],
                  2 => [1, 3, 2, 8],
                  3 => [3, 11, 13, 2],
                  4 => [4, 8, 5, 10],
                  5 => [8, 2, 7, 5],
                  6 => [2, 13, 6, 7],
                  7 => [5, 7, 12],
                  8 => [7, 6, 14, 12],
                  9 => [12, 14, 9]);

element_types = Dict(
                       1 => :Quad4,
                       2 => :Quad4,
                       3 => :Quad4,
                       4 => :Quad4,
                       5 => :Quad4,
                       6 => :Quad4,
                       7 => :Tri3,
                       8 => :Quad4,
                       9 => :Tri3);

P = 15
```

Now we can start to use the functions of NodeNumbering. First we use 
`create_adjacency_graph(elements, element_types)` to create the adjacency graph which 
shows the original node adjacencies in the mesh.
Then using `node_degrees(adjacency)` we list the degrees of all nodes in the mesh.
The function `RCM(adjacency, degrees, P) ` does the Reverse-CuthillMcKee ordering for 
our nodes. 
Next using `renumbering(neworder)` we will give the RCM ordered nodes new ID:s from 
1 to 15.
`create_RCM_adjacency(adjacency, finalorder)` creates the new adjacency graph for the 
RCM ordered and renamed nodes.
The result can be visualized as a matrix with `adjacency_visualization(RCM_adjacency) ` 
function.
Finally if we want to plot the result matrix we can use the PyPlot function 
`matshow(matrix_name)`

```julia
using NodeNumbering: create_adjacency_graph, node_degrees, RCM, renumbering,
create_RCM_adjacency, adjacency_visualization
using PyPlot: matshow

adjacency = create_adjacency_graph(elements, element_types)
degrees = node_degrees(adjacency)
neworder = RCM(adjacency, degrees, P)
finalorder = renumbering(neworder)
RCM_adjacency = create_RCM_adjacency(adjacency, finalorder)
newmatrix = adjacency_visualization(RCM_adjacency)
matshow(newmatrix)
```

The figure below shows the original adjacency graph and the new RCM ordered graph as matrices.

<img src="{{ site.url }}/assets/2017-08-29-reordering-nodes-with-the-RCM-algorithm/matrices.PNG">

# References

Wikimedia commons: Cuthill-McKee algorithm
https://en.wikipedia.org/wiki/Cuthill%E2%80%93McKee_algorithm