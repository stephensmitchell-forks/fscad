# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fscad import *

import adsk.fusion
import unittest
import test_utils
import importlib
importlib.reload(test_utils)
import test_utils


class PlaceTest(test_utils.FscadTestCase):
    def test_place(self):
        box1 = Box(1, 2, 3, "box1")
        box2 = Box(5, 6, 7, "box2")

        box2.place(-box2 == ~box1,
                   ~box2 == +box1,
                   +box2 == -box1)

        self.assertEqual(box2.size().asArray(), (5, 6, 7))
        self.assertEqual(box2.min().asArray(), (.5, 2 - 6/2, -7))
        self.assertEqual(box2.mid().asArray(), (.5 + 5/2, 2, -7/2))
        self.assertEqual(box2.max().asArray(), (.5 + 5, 2 + 6/2, 0))

        box1.create_occurrence()
        box2.create_occurrence()

    def test_place_offset(self):
        box1 = Box(1, 1, 1, "box1")
        box2 = Box(1, 1, 1, "box2")
        box2.place(
            (-box2 == +box1) + 1,
            ~box2 == ~box1,
            ~box2 == ~box1)
        box1.create_occurrence()
        box2.create_occurrence()

    def test_place_children(self):
        box1 = Box(1, 1, 1, "box1")
        box2 = Box(1, 1, 1, "box2")
        box2.place(
            (-box2 == +box1),
            ~box2 == ~box1,
            ~box2 == ~box1)
        union = Union(box1, box2)

        box3 = Box(1, 1, 1, "box3")

        union.place(-union == +box3,
                    ~union == ~box3,
                    ~union == ~box3)
        union.add(box3)

        self.assertEqual(box1.size().asArray(), (1, 1, 1))
        self.assertEqual(box1.min().asArray(), (1, 0, 0))
        self.assertEqual(box1.mid().asArray(), (1.5, .5, .5))
        self.assertEqual(box1.max().asArray(), (2, 1, 1))

        union.create_occurrence(True)

from test_utils import load_tests
def run(context):
    import sys
    test_suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(failfast=True).run(test_suite)
