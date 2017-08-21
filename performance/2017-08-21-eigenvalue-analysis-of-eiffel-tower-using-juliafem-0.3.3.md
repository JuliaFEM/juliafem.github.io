---
layout: post
author: Jukka Aho
title: Eigenvalue analysis of Eiffel tower
date: 2017-08-21
comments: true
categories: performance eiffel-tower v0.3.3
---

Eigenvalue analysis of Eiffel tower is done using JuliaFEM 0.3.3 and Julia 0.6.
Assembly of global matrices and writing results is optimized a bit. Results show
that when models are big enough, solution of eigenvalue problem takes about 80 %
of time.

<!-- more -->

## Code

```julia
using JuliaFEM
using JuliaFEM.Preprocess
using JuliaFEM.Postprocess

#model = "EIFFEL_TOWER_TET10_220271"
model = ARGS[1]
mesh = joinpath("eiffel-tower", "$model.inp")
results = "$model"

@timeit "run performance test" begin

@timeit "parse input data" begin
    mesh = abaqus_read_mesh(mesh)
    for (nid, ncoords) in mesh.nodes
        mesh.nodes[nid] = 304.8 * ncoords
    end
    info("element sets = ", collect(keys(mesh.element_sets)))
    info("surface sets = ", collect(keys(mesh.surface_sets)))
end

@timeit "initialize model" begin
    tower = Problem(Elasticity, "tower", 3)
    tower.elements = create_elements(mesh, "TOWER")
    update!(tower, "youngs modulus", 210.0E3)
    update!(tower, "poissons ratio", 0.3)
    update!(tower, "density", 7.85E-9)

    support = Problem(Dirichlet, "fixed", 3, "displacement")
    support.elements = create_surface_elements(mesh, "SUPPORT")
    update!(support, "geometry", mesh.nodes)
    update!(support, "displacement 1", 0.0)
    update!(support, "displacement 2", 0.0)
    update!(support, "displacement 3", 0.0)
end

@timeit "solve eigenvalue problem" begin
    solver = Solver(Modal, tower, support)
    solver.xdmf = Xdmf(results; overwrite=true)
    solver.properties.nev = 5
    solver.properties.which = :SM
    solver()
    println("Eigenvalues: ", sqrt.(solver.properties.eigvals) / (2*pi))
end

end

print_timer()
```

## Results

**220271 nodes**

```
Eigenvalues: [0.554667, 0.557987, 1.59926, 1.60043, 2.37304]
 ──────────────────────────────────────────────────────────────────────────────
                                       Time                   Allocations
                               ──────────────────────   ───────────────────────
       Tot / % measured:        18436996367s / 0.00%        46.1GiB / 97.8%

 Section               ncalls     time   %tot     avg     alloc   %tot      avg
 ──────────────────────────────────────────────────────────────────────────────
 run performance test       1     122s   100%    122s   45.1GiB  100%   45.1GiB
   solve eigenvalue...      1     116s  95.2%    116s   44.3GiB  98.1%  44.3GiB
     assemble matrices      1    46.0s  37.8%   46.0s   24.6GiB  54.5%  24.6GiB
       assemble tow...      1    22.3s  18.3%   22.3s   14.0GiB  31.0%  14.0GiB
       assemble tower       1    16.4s  13.5%   16.4s   5.10GiB  11.3%  5.10GiB
       assemble fixed       1    334ms  0.27%   334ms   14.6MiB  0.03%  14.6MiB
     solve eigenval...      1    37.9s  31.1%   37.9s   8.92GiB  19.8%  8.92GiB
     eliminate boun...      1    10.4s  8.50%   10.4s   5.11GiB  11.3%  5.11GiB
     save results t...      1    6.39s  5.24%   6.39s    793MiB  1.72%   793MiB
       fetch geometry       1    2.94s  2.42%   2.94s    298MiB  0.65%   298MiB
       save modes           1    1.55s  1.27%   1.55s    336MiB  0.73%   336MiB
         store eige...      5    689ms  0.57%   138ms    287MiB  0.62%  57.4MiB
           create m...      5    646ms  0.53%   129ms    260MiB  0.56%  52.1MiB
         save topol...      5    261ms  0.21%  52.1ms   28.1MiB  0.06%  5.62MiB
         save topol...      5   26.6ms  0.02%  5.32ms   77.7KiB  0.00%  15.5KiB
       create topol...      1    1.25s  1.02%   1.25s    108MiB  0.23%   108MiB
       create node ...      1    122ms  0.10%   122ms   16.0MiB  0.03%  16.0MiB
       create ncoor...      1    106ms  0.09%   106ms   25.7MiB  0.06%  25.7MiB
   parse input data         1    4.77s  3.92%   4.77s    689MiB  1.49%   689MiB
   initialize model         1    1.13s  0.93%   1.13s    180MiB  0.39%   180MiB
 ──────────────────────────────────────────────────────────────────────────────
```

**376120 nodes**

```
Eigenvalues: [0.548343, 0.548526, 1.56613, 1.56662, 2.32376]
 ──────────────────────────────────────────────────────────────────────────────
                                       Time                   Allocations
                               ──────────────────────   ───────────────────────
       Tot / % measured:        18436996624s / 0.00%        81.2GiB / 98.7%

 Section               ncalls     time   %tot     avg     alloc   %tot      avg
 ──────────────────────────────────────────────────────────────────────────────
 run performance test       1     231s   100%    231s   80.2GiB  100%   80.2GiB
   solve eigenvalue...      1     221s  96.0%    221s   78.7GiB  98.1%  78.7GiB
     assemble matrices      1    87.1s  37.7%   87.1s   43.8GiB  54.6%  43.8GiB
       assemble tow...      1    44.0s  19.1%   44.0s   24.5GiB  30.6%  24.5GiB
       assemble tower       1    23.1s  10.0%   23.1s   9.59GiB  12.0%  9.59GiB
       assemble fixed       1    386ms  0.17%   386ms   44.0MiB  0.05%  44.0MiB
     solve eigenval...      1    74.7s  32.4%   74.7s   16.5GiB  20.6%  16.5GiB
     eliminate boun...      1    22.9s  9.93%   22.9s   8.78GiB  11.0%  8.78GiB
     save results t...      1    13.6s  5.89%   13.6s   1.34GiB  1.67%  1.34GiB
       fetch geometry       1    6.69s  2.90%   6.69s    535MiB  0.65%   535MiB
       save modes           1    3.68s  1.59%   3.68s    558MiB  0.68%   558MiB
         store eige...      5    2.82s  1.22%   565ms    489MiB  0.60%  97.7MiB
           create m...      5    2.74s  1.19%   547ms    445MiB  0.54%  88.9MiB
         save topol...      5    349ms  0.15%  69.7ms   41.8MiB  0.05%  8.36MiB
         save topol...      5   46.3ms  0.02%  9.25ms    164KiB  0.00%  32.7KiB
       create topol...      1    2.03s  0.88%   2.03s    190MiB  0.23%   190MiB
       create ncoor...      1    489ms  0.21%   489ms   43.5MiB  0.05%  43.5MiB
       create node ...      1    150ms  0.07%   150ms   33.0MiB  0.04%  33.0MiB
   parse input data         1    7.44s  3.22%   7.44s   1.20GiB  1.50%  1.20GiB
   initialize model         1    1.88s  0.82%   1.88s    316MiB  0.38%   316MiB
 ──────────────────────────────────────────────────────────────────────────────
```

**921317 nodes**

```
Eigenvalues: [0.542289, 0.542386, 1.54818, 1.54852, 2.26661]
 ──────────────────────────────────────────────────────────────────────────────
                                       Time                   Allocations
                               ──────────────────────   ───────────────────────
       Tot / % measured:        18436997275s / 0.00%         204GiB / 99.5%

 Section               ncalls     time   %tot     avg     alloc   %tot      avg
 ──────────────────────────────────────────────────────────────────────────────
 run performance test       1     627s   100%    627s    203GiB  100%    203GiB
   solve eigenvalue...      1     604s  96.4%    604s    199GiB  98.2%   199GiB
     assemble matrices      1     231s  36.8%    231s    108GiB  53.2%   108GiB
       assemble tow...      1     126s  20.1%    126s   62.4GiB  30.8%  62.4GiB
       assemble tower       1    50.0s  7.97%   50.0s   20.7GiB  10.2%  20.7GiB
       assemble fixed       1    518ms  0.08%   518ms    151MiB  0.07%   151MiB
     solve eigenval...      1     205s  32.7%    205s   45.6GiB  22.5%  45.6GiB
     eliminate boun...      1    80.3s  12.8%   80.3s   21.8GiB  10.8%  21.8GiB
     save results t...      1    36.8s  5.86%   36.8s   3.27GiB  1.61%  3.27GiB
       save modes           1    13.2s  2.11%   13.2s   1.30GiB  0.64%  1.30GiB
         store eige...      5    12.0s  1.91%   2.40s   1.17GiB  0.58%   239MiB
           create m...      5    11.7s  1.87%   2.35s   1.06GiB  0.52%   218MiB
         save topol...      5    450ms  0.07%  89.9ms   83.5MiB  0.04%  16.7MiB
         save topol...      5    116ms  0.02%  23.3ms    496KiB  0.00%  99.2KiB
       fetch geometry       1    12.1s  1.93%   12.1s   1.31GiB  0.65%  1.31GiB
       create ncoor...      1    3.14s  0.50%   3.14s    106MiB  0.05%   106MiB
       create topol...      1    2.66s  0.42%   2.66s    485MiB  0.23%   485MiB
       create node ...      1    232ms  0.04%   232ms   67.0MiB  0.03%  67.0MiB
   parse input data         1    18.7s  2.98%   18.7s   2.94GiB  1.45%  2.94GiB
   initialize model         1    3.71s  0.59%   3.71s    802MiB  0.39%   802MiB
 ──────────────────────────────────────────────────────────────────────────────
```

**1327989 nodes**

```
Eigenvalues: [0.541056, 0.541163, 1.54381, 1.54408, 2.25313]
 ──────────────────────────────────────────────────────────────────────────────
                                       Time                   Allocations
                               ──────────────────────   ───────────────────────
       Tot / % measured:        18436998213s / 0.00%         307GiB / 100%

 Section               ncalls     time   %tot     avg     alloc   %tot      avg
 ──────────────────────────────────────────────────────────────────────────────
 run performance test       1     905s   100%    905s    306GiB  100%    306GiB
   solve eigenvalue...      1     873s  96.5%    873s    301GiB  98.3%   301GiB
     solve eigenval...      1     350s  38.7%    350s   71.8GiB  23.5%  71.8GiB
     assemble matrices      1     256s  28.3%    256s    168GiB  54.9%   168GiB
       assemble tow...      1     135s  14.9%    135s   94.5GiB  30.9%  94.5GiB
       assemble tower       1    73.6s  8.13%   73.6s   36.7GiB  12.0%  36.7GiB
       assemble fixed       1    680ms  0.08%   680ms    229MiB  0.07%   229MiB
     eliminate boun...      1     115s  12.7%    115s   26.4GiB  8.64%  26.4GiB
     save results t...      1    65.9s  7.28%   65.9s   4.71GiB  1.54%  4.71GiB
       save modes           1    29.8s  3.29%   29.8s   1.87GiB  0.61%  1.87GiB
         store eige...      5    27.9s  3.09%   5.59s   1.68GiB  0.55%   345MiB
           create m...      5    27.5s  3.04%   5.51s   1.53GiB  0.50%   314MiB
         save topol...      5    830ms  0.09%   166ms    129MiB  0.04%  25.8MiB
         save topol...      5    206ms  0.02%  41.1ms    887KiB  0.00%   177KiB
       fetch geometry       1    20.6s  2.27%   20.6s   1.89GiB  0.62%  1.89GiB
       create topol...      1    8.58s  0.95%   8.58s    724MiB  0.23%   724MiB
       create ncoor...      1    4.74s  0.52%   4.74s    152MiB  0.05%   152MiB
       create node ...      1    581ms  0.06%   581ms   67.0MiB  0.02%  67.0MiB
   parse input data         1    27.0s  2.98%   27.0s   4.19GiB  1.37%  4.19GiB
   initialize model         1    4.84s  0.53%   4.84s   1.16GiB  0.38%  1.16GiB
 ──────────────────────────────────────────────────────────────────────────────
```

**2357071 nodes**

```
 ──────────────────────────────────────────────────────────────────────────────
                                       Time                   Allocations
                               ──────────────────────   ───────────────────────
       Tot / % measured:        18437001397s / 0.00%         587GiB / 100%

 Section               ncalls     time   %tot     avg     alloc   %tot      avg
 ──────────────────────────────────────────────────────────────────────────────
 run performance test       1    3158s   100%   3158s    586GiB  100%    586GiB
   solve eigenvalue...      1    3112s  98.5%   3112s    576GiB  98.3%   576GiB
     solve eigenval...      1    1381s  43.7%   1381s    149GiB  25.5%   149GiB
     assemble matrices      1     928s  29.4%    928s    306GiB  52.2%   306GiB
       assemble tow...      1     589s  18.6%    589s    174GiB  29.6%   174GiB
       assemble tower       1     143s  4.52%    143s   63.5GiB  10.8%  63.5GiB
       assemble fixed       1    902ms  0.03%   902ms    401MiB  0.07%   401MiB
     eliminate boun...      1     381s  12.1%    381s   58.0GiB  9.90%  58.0GiB
     save results t...      1     206s  6.51%    206s   8.66GiB  1.48%  8.66GiB
       save modes           1    78.6s  2.49%   78.6s   3.32GiB  0.57%  3.32GiB
         store eige...      5    75.1s  2.38%   15.0s   2.99GiB  0.51%   612MiB
           create m...      5    73.3s  2.32%   14.7s   2.72GiB  0.46%   557MiB
         save topol...      5    2.16s  0.07%   433ms    236MiB  0.04%  47.3MiB
         save topol...      5    358ms  0.01%  71.5ms   1.63MiB  0.00%   335KiB
       fetch geometry       1    64.6s  2.04%   64.6s   3.58GiB  0.61%  3.58GiB
       create ncoor...      1    22.9s  0.72%   22.9s    270MiB  0.05%   270MiB
       create topol...      1    22.1s  0.70%   22.1s   1.32GiB  0.23%  1.32GiB
       create node ...      1    14.5s  0.46%   14.5s    135MiB  0.02%   135MiB
   parse input data         1    38.2s  1.21%   38.2s   7.75GiB  1.32%  7.75GiB
   initialize model         1    7.85s  0.25%   7.85s   2.17GiB  0.37%  2.17GiB
 ──────────────────────────────────────────────────────────────────────────────
```

**3640549 nodes**
```
 ──────────────────────────────────────────────────────────────────────────────
                                       Time                   Allocations
                               ──────────────────────   ───────────────────────
       Tot / % measured:        18436983005s / 0.00%         805GiB / 100%

 Section               ncalls     time   %tot     avg     alloc   %tot      avg
 ──────────────────────────────────────────────────────────────────────────────
 run performance test       1    9182s   100%   9182s    804GiB  100%    804GiB
   solve eigenvalue...      1    9133s  99.5%   9133s    788GiB  98.0%   788GiB
     solve eigenval...      1    7484s  81.5%   7484s    279GiB  34.7%   279GiB
     assemble matrices      1     580s  6.32%    580s    318GiB  39.5%   318GiB
       assemble tower       1     220s  2.40%    220s   93.2GiB  11.6%  93.2GiB
       assemble tow...      1     188s  2.04%    188s    114GiB  14.1%   114GiB
       assemble fixed       1    1.17s  0.01%   1.17s    586MiB  0.07%   586MiB
     save results t...      1     377s  4.11%    377s   13.8GiB  1.72%  13.8GiB
       fetch geometry       1     143s  1.56%    143s   5.90GiB  0.73%  5.90GiB
       save modes           1     135s  1.47%    135s   5.08GiB  0.63%  5.08GiB
         store eige...      5     129s  1.41%   25.8s   4.61GiB  0.57%   944MiB
           create m...      5     127s  1.39%   25.5s   4.20GiB  0.52%   861MiB
         save topol...      5    3.34s  0.04%   669ms    326MiB  0.04%  65.1MiB
         save topol...      5    582ms  0.01%   116ms   1.79MiB  0.00%   366KiB
       create topol...      1    40.7s  0.44%   40.7s   2.13GiB  0.26%  2.13GiB
       create ncoor...      1    35.2s  0.38%   35.2s    417MiB  0.05%   417MiB
       create node ...      1    18.3s  0.20%   18.3s    271MiB  0.03%   271MiB
     eliminate boun...      1     326s  3.55%    326s   91.6GiB  11.4%  91.6GiB
   parse input data         1    40.1s  0.44%   40.1s   12.5GiB  1.56%  12.5GiB
   initialize model         1    8.80s  0.10%   8.80s   3.51GiB  0.44%  3.51GiB
 ──────────────────────────────────────────────────────────────────────────────
```

## Further analysis and discussion

<img src="{{ site.url }}/assets/2017-08-21-eigenvalue-analysis-of-eiffel-tower-using-juliafem-0.3.3/results.png">

Dashed results are calculated using JuliaFEM 0.3.2 and solid lines are for 0.3.3.

Assemly of stiffness and mass matrix is optimized without sacrificing readablity
of code (too much). It can still be optimized more to get even better performance,
or run assembler using threads. The results however shows that vast major of the
time is spend in a single command `eigs(K, M)`. So when model sizes are **realistic**,
the assembly time is under 10 % of total solution time. The result is totally
different compared to small toy models, where assembly time can be over 50 % of
total solution time. That's the reason why performance tests must be done using full
size models.

Conclusions are, that we get 80-90 % of performance with 10 % of effort using dynamic
language like Julia. The performance penalty, compared to some statically typed
languages like FORTRAN or C, is acceptable by taking into account that development
time of the software itself is reduced dramatically.

Next steps are to optimize memory usage during the solution of eigenmodes to be able
to calculate even bigger models.