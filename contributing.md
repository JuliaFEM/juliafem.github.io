---
layout: page
title: Contributing
permalink: /contributing/
---

Contributing to JuliaFEM works in the same way as contributing to other open-source
projects, so instructions to contribute follows closely to what is described for
other packages.
We use `Documenter.jl` to document packages, so it is worth reading
[Coding style guide](https://juliadocs.github.io/Documenter.jl/stable/man/contributing/).
There are hundreds of tutorials on using `git` and [ProGit](https://git-scm.com/book/en/v2)
is available for free online.

**You can always ask for
assistance from our [Gitter channel](https://gitter.im/JuliaFEM/JuliaFEM.jl).**

The basic steps for contributing to JuliaFEM are listed below:

1. Create an account or sign in to [GitHub](https://github.com/).

2. Go to the [Git home page](http://git-scm.com/) and download the Git installer.
   Run the installer to get Git on your computer. It is a version control system
   used by GitHub. To learn its basics, go through this
   [Git tutorial](https://try.github.io/levels/1/challenges/1>). Another option
   is to install e.g. [SourceTree](https://www.sourcetreeapp.com/). Now you should
   have a `Git Bash` in your computer.

3. Download and install Julia (v0.6+) onto your computer. You can get the latest
   version from [here](https://julialang.org/downloads/). From [Julia
   README](https://github.com/JuliaLang/julia/blob/master/README.md) you will
   find the complete instructions for installing it for your platform.

4. Go to the [JuliaFEM GitHub page](https://github.com/JuliaFEM/JuliaFEM.jl>).
   At the top-right corner, press the `Fork`-button to fork your own copy of
   JuliaFEM to your own account.

5. Clone JuliaFEM from your repository to your computer. Navigate to the folder
   you want to clone it to, and type the following command (inserting your GitHub
   username to its place):

   `git clone https://github.com/your_github_username/JuliaFEM.jl.git`
    
   Alternatively, you can clone the package using Julia's command

   `Pkg.clone("https://github.com/your_github_username/JuliaFEM.jl`

   In the latter case, package will go to somewhat hidden place
   `~/.julia/v0.6/JuliaFEM`.

   Notice, that if you clone repository to some non-standard location, you must make
   julia aware of the new package location by a modifying `LOAD_PATH`. For example,
   if you have JuliaFEM cloned to `~/repositories/JuliaFEM`, you need to
   `push!(LOAD_PATH, joinpath(homedir(), "repositories")` before using JuliaFEM.
   
   If you have already installed JuliaFEM using `Pkg.add` you can simply edit that copy,
   but you will have to push changes to your forked version as you would not have commit
   access to the repositories under the JuliaFEM organization.
   Add your fork as remote repository for the JuliaFEM repository on your local computer:

   `git remote add USERNAME https://github.com/USERNAME/JuliaFEM.jl.git`

   After that you can push the changes to your fork by `git push USERNAME master`.
   
   Make sure that you do not have multiple copies of JuliaFEM on your system,
   i.e. one copy
   in `~/.julia/v0.6/JuliaFEM` and other one in `~/repositories/JuliaFEM`. If that
   is the case, you can rename the directory not to keep and after that make Julia
   aware of JuliaFEM by making for example symbolic link to `~/.julia/v0.6` if
   keeping the copy located in outside of Julia's package directory or add
   non-standard path to `LOAD_PATH` as explained above.

6. You can now navigate to JuliaFEM in the folder you chose at step 5. There
   you will find the same contents as you see in your GitHub JuliaFEM repository.
   Now, locate the file you want to modify, open it with your desired text
   editor, make the changes and save the new version. If you type `git status`,
   you will see that the files you have created or modified are listed under `untracked files`.

7. Add the files you want to update to the staging area by typing
   `git add <file1> <file2>...`. If you type `git status`, you will see that
   the files added to the staging area are listed under `Changes to be committed`.
   This process also supports wildcard symbols. If you want to remove a file
   from the staging area, type `git reset <file>`.

8. To store the staged files, commit the files to your repository and add a
   description message by typing `git commit -m "your_message_here"`. The
   message should describe the changes that were made.

9. When you are happy with the commits and want to update them to your
   repository, type `git push`.

10. Go to your GitHub JuliaFEM repository. You'll notice that the commit you
    have made and pushed is now visible above the JuliaFEM file branch. If you
    click the ``latest commit`` link, you can see the changes made to the file.
    Finally, click ``Pull request`` to create a pull request of the commits
    you've made, so that other contributors can review it.

11. If other contributors ask you to make changes to your pull request, just
    repeat steps 6-9. Your commits will be updated to your original pull request.
    Do this until everyone is satisfied and your pull request can be merged to
    the master branch.

There are also some GUI apps to use git if you do not feel comfortable using the terminal.
For OSX and Windows a good application is [SourceTree](https://www.sourcetreeapp.com),
for Linux, maybe [SmartGit](http://www.syntevo.com/smartgit/) will work. GitHub
has also desktop application.


### Details of contibuting to JuliaFEM

Travis-CI runs [PkgTestSuite.jl](https://github.com/JuliaFEM/PkgTestSuite.jl) to
verify the quality of code, so it is good idea to run that on own local computer
before making a pull request. PkgTestSuite tests that all tests pass.
Some more tests are performed like testing that all source files have proper
licence headers and no tabs has been used in code. If you have already done
pull request, you can inspect from travis if the build fail to find out the cause
of failure.

#### Don't use utf-8 characters in program code

We are not using utf-8 characters.
See issue [#18](https://github.com/JuliaFEM/JuliaFEM.jl/issues/18).

#### Supported Julia versions
We support Julia versions 0.6+.
See issue [#26](https://github.com/JuliaFEM/JuliaFEM.jl/issues/26).

#### Use only pull requests, never push to master
See issue [#29](https://github.com/JuliaFEM/JuliaFEM.jl/issues/29). This
ensures peer review check for contributors and hopefully will decrease the
number of merge conflicts. Before making the pull request run all tests:
either type `julia> Pkg.test("JuliaFEM")` at REPL or `julia test/runtests.jl` at
command line. 

#### New technology is recommended to be introduced through notebooks
See issue [#12](https://github.com/JuliaFEM/JuliaFEM.jl/issues/12). Idea is
to introduce new technology as a notebook for the very beginning. Then when it's
get mature the notebook will serve functional test for the matter. All notebooks
will be included as examples to the documentation. 

#### Write unit tests for a package
See issue [#27](https://github.com/JuliaFEM/JuliaFEM.jl/issues/27). We believe
into Test Driven Development (TDD), thus 100 % test coverage is the ultimate goal. 

#### JuliaFEM.jl is using Logging.jl
See issue [#25](https://github.com/JuliaFEM/JuliaFEM.jl/issues/25). We have
written a test to check all sources in src folder to find any print statements.
Use `Logging.jl` instead of `println()`. No use of `println()` is allowed in code.

#### Code indentation
We use 4 spaces like in Python. See issue [#5](https://github.com/JuliaFEM/JuliaFEM.jl/issues/5).

#### Write docstrings for function
Docstrings help people to understand how functions works and they are a crucial
part of quality code. See issue [#](https://github.com/JuliaFEM/JuliaFEM.jl/issues/5).
For a good introduction how to write good docstrings, see the official Julia documentation
about [docstrings](https://docs.julialang.org/en/stable/manual/documentation/).

#### Documentation
We use MarkDown syntax to document projects. Information how to write markdown
format is described on internet. [Here](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf)
is markdown cheatsheet. See issue [#49](https://github.com/JuliaFEM/JuliaFEM.jl/issues/49).

#### Line width
This is not (yet) strict requirement, but try to keep line width max 80 characters, like
in Python.

### For performance critical functions use @inferred
See issue [#90](https://github.com/JuliaFEM/JuliaFEM.jl/issues/90). This macro tests that
the expression that it is called on returns the same type as that inferred by the compiler.
It is useful to check for type stability.

### References

* https://try.github.io/levels/1/challenges/1
