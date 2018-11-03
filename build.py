#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    shared_option_name = False if platform.system() == "Windows" else "TBB:shared"
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name=shared_option_name, pure_c=False)
    builder.run()
