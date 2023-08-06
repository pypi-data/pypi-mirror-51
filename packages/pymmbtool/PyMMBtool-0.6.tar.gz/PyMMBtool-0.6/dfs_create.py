#!/usr/bin/python
#===============================================================================
# Copyright (C) 2012-2018 Adrian Hungate
#
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#===============================================================================
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

import PyMMB
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Syntax: %s <disc.ssd> <title> [(40|80)]" % sys.argv[0]
        sys.exit()
    if len(sys.argv) == 3:
        tracks = 80
    else:
        tracks = int(sys.argv[3])
    DFS = PyMMB.dfs.dfs.new(sys.argv[1], title = sys.argv[2], tracks = tracks)
