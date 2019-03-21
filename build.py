#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(pure_c=False)
    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        options["TBB:tbbmalloc"] = False
        filtered_builds.append([settings, copy.copy(options), env_vars, build_requires])
        options["TBB:tbbmalloc"] = True
        filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()
