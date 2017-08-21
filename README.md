# juliafem.github.io / www.juliafem.org

Web pages for organization. The actual page is juliafem.github.io and www.juliafem.org is pointing
to same site.

## Adding content

**for contributors**: If you have all [Jekyll](https://jekyllrb.com/) related stuff installed on
local machine (computer you are using to develop), you can do `bundle exec jekyll serve` and check
using your web browser from url address `localhost:4000`, (i.e. write to address bar `http://localhost:4000`)
that content is OK. **If that is the case**, you can then push directly to the
master. **Otherwise**, create branch to repository [juliafem.github.io](https://github.com/JuliaFEM/juliafem.github.io),
do changes, make pull request and ask someone to review changes locally before merging.

**for others**: Fork, do local changes, do pull request. If you want to be extra helpful and have
installed Jekyll things on local machine, you can add screenshot of page to PR to make it easier
for reviewers.

Examples can be written using Jupyter Notebooks or Markdown. See
`examples/2017-08-06-instructions-how-to-write-examples` how to write using Jupyter and
`performance/2017-08-13-eigenvalue-analysis-of-eiffel-tower-using-juliafem-0.3.2.md` how to write
using Markdown syntax.

## Adding images

Place your video/image to
```
    <REPO_DIR>/assets/<blog-post>/<myimg>.png
```

For example, if the blog post name is
    `2017-08-13-eigenvalue-analysis-of-eiffel-tower-using-juliafem-0.3.2`
and you want to add image
    `eiffel_model.png`,
the correct path is
```
    <REPO_DIR>/assets/2017-08-13-eigenvalue-analysis-of-eiffel-tower-using-juliafem-0.3.2/eiffel_model.png
```

`REPO_DIR` is the directory where `juliafem.github.io` is cloned.

Then, to point that image inside blog post, use the following format:
```
<img src="/assets/<blog-post>/<myimg>.png">
```

For example, using the example above, the corresponding tag would be:
```
<img src="/assets/2017-08-13-eigenvalue-analysis-of-eiffel-tower-using-juliafem-0.3.2/eiffel_model.png">
```

Also, it's a very good idea to watermark at least the most important pictures
with JuliaFEM logo (can be found from /assets/) and maybe who has done the
simulation, where, and so on.
