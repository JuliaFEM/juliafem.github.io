#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import json
import urllib.request


__template__ = """\
---
layout: page
title: {name}
---

{description}
"""


def main(args):
    url = "https://api.github.com/orgs/%s/repos" % args.organization
    resp = urllib.request.urlopen(url).read()
    data = json.loads(resp)
    for d in data:
        s = d["name"].lower().replace(".jl","")
        fn = os.path.join(args.path, "%012i_%s.md" % (d["id"], s))
        with open(fn, "w") as fh:
            fh.write(__template__.format(**d))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse GitHub organization and create project pages for Jekyll")
    parser.add_argument("organization", type=str, help="Organization name")
    parser.add_argument("path", type=str, help="Output directory for pages")
    args = parser.parse_args()
    main(args)
