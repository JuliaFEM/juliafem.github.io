---
layout: page
title: Summer of Code
permalink: /JFSoC/
---

Here we list the Summer of Code projects

## 2017

This summer I got to be a part of the JuliaFEM project. My main responsibilities where to code two 
repositories: NodeNumbering.jl and ModelReduction.jl. I also wrote [a paper](https://doi.org/10.23998/rm.65040) about calculating natural 
frequencies with JuliaFEM and improved the documentation and examples of JuliaFEM.

NodeNumbering.jl contains functions to perform the Reverse Cuthill-McKee algorithm which is used to 
reduce the bandwidth of sparse matrices. At the moment the package has 8 merged functions. The figure 
below shows how matrix bandwidth is reduced with the code.

<img src="{{ site.url }}/assets/JFSoC/matrices.png">

ModelReduction.jl is a repository to reduce the dimension of a model for multibody dynamics problems. 
The package includes e.g. the Guyan reduction and the Craig-Bampton method. The package has 6 merged 
functions.

This summer I got great guidance from Tero and Jukka who taught me a lot. I learned how to use Github 
properly and how to perform the whole coding process with the right working methods. My coding skills 
progressed significantly and I learned a whole new coding language. 

I am very happy that I got to be a contributor in the JuliaFEM project and I will definitely be a part 
of the JuliaFEM team also in the future and keep developing and improving it to be the best open source 
FEM solver in the world. 

Marja Rapo,

Engineering Mechanics student at University of Oulu

marja@juliafem.org
