"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from cvxpy.atoms import *
from cvxpy.expressions.variables import Variable
import cvxpy.utilities as u
import cvxpy.interface.matrix_utilities as intf
import unittest

class TestAtoms(unittest.TestCase):
    """ Unit tests for the atoms module. """
    def setUp(self):
        self.a = Variable(name='a')

        self.x = Variable(2, name='x')
        self.y = Variable(2, name='y')

        self.A = Variable(2,2,name='A')
        self.B = Variable(2,2,name='B')
        self.C = Variable(3,2,name='C')

    # Test the norm wrapper.
    def test_norm(self):
        with self.assertRaises(Exception) as cm:
            norm(self.C, 3)
        self.assertEqual(str(cm.exception),
            "Invalid value 3 for p.")

    # Test the normInf class.
    def test_normInf(self):
        exp = self.x+self.y
        atom = normInf(exp)
        # self.assertEquals(atom.name(), "normInf(x + y)")
        self.assertEquals(atom.size, (1,1))
        self.assertEquals(atom.curvature, u.Curvature.CONVEX)
        self.assertEquals(normInf(atom).curvature, u.Curvature.CONVEX)
        self.assertEquals(normInf(-atom).curvature, u.Curvature.CONVEX)

    # Test the norm1 class.
    def test_norm1(self):
        exp = self.x+self.y
        atom = norm1(exp)
        # self.assertEquals(atom.name(), "norm1(x + y)")
        self.assertEquals(atom.size, (1,1))
        self.assertEquals(atom.curvature, u.Curvature.CONVEX)
        self.assertEquals(norm1(atom).curvature, u.Curvature.CONVEX)
        self.assertEquals(norm1(-atom).curvature, u.Curvature.CONVEX)

    # Test the norm2 class.
    def test_norm2(self):
        exp = self.x+self.y
        atom = norm2(exp)
        # self.assertEquals(atom.name(), "norm2(x + y)")
        self.assertEquals(atom.size, (1,1))
        self.assertEquals(atom.curvature, u.Curvature.CONVEX)
        self.assertEquals(norm2(atom).curvature, u.Curvature.CONVEX)
        self.assertEquals(norm2(-atom).curvature, u.Curvature.CONVEX)

    # Test quad_over_lin DCP.
    def test_quad_over_lin(self):
        atom = quad_over_lin(square(self.x), self.a)
        self.assertEquals(atom.curvature, u.Curvature.CONVEX)
        atom = quad_over_lin(-square(self.x), self.a)
        self.assertEquals(atom.curvature, u.Curvature.CONVEX)
        atom = quad_over_lin(sqrt(self.x), self.a)
        self.assertEquals(atom.curvature, u.Curvature.UNKNOWN)

    # Test sign logic for max.
    def test_max_sign(self):
        # One arg.
        self.assertEquals(max(1).sign, u.Sign.POSITIVE)
        self.assertEquals(max(-2).sign, u.Sign.NEGATIVE)
        self.assertEquals(max(Variable()).sign, u.Sign.UNKNOWN)
        self.assertEquals(max(0).sign, u.Sign.ZERO)

        # Two args.
        self.assertEquals(max(1, 2).sign, u.Sign.POSITIVE)
        self.assertEquals(max(1, Variable()).sign, u.Sign.POSITIVE)
        self.assertEquals(max(1, -2).sign, u.Sign.POSITIVE)
        self.assertEquals(max(1, 0).sign, u.Sign.POSITIVE)

        self.assertEquals(max(Variable(), 0).sign, u.Sign.POSITIVE)
        self.assertEquals(max(Variable(), Variable()).sign, u.Sign.UNKNOWN)
        self.assertEquals(max(Variable(), -2).sign, u.Sign.UNKNOWN)

        self.assertEquals(max(0, 0).sign, u.Sign.ZERO)
        self.assertEquals(max(0, -2).sign, u.Sign.ZERO)

        self.assertEquals(max(-3, -2).sign, u.Sign.NEGATIVE)

        # Many args.
        self.assertEquals(max(-2, Variable(), 0, -1, Variable(), 1).sign,
                          u.Sign.POSITIVE)

    # Test sign logic for min.
    def test_min_sign(self):
        # One arg.
        self.assertEquals(min(1).sign, u.Sign.POSITIVE)
        self.assertEquals(min(-2).sign, u.Sign.NEGATIVE)
        self.assertEquals(min(Variable()).sign, u.Sign.UNKNOWN)
        self.assertEquals(min(0).sign, u.Sign.ZERO)

        # Two args.
        self.assertEquals(min(1, 2).sign, u.Sign.POSITIVE)
        self.assertEquals(min(1, Variable()).sign, u.Sign.UNKNOWN)
        self.assertEquals(min(1, -2).sign, u.Sign.NEGATIVE)
        self.assertEquals(min(1, 0).sign, u.Sign.ZERO)

        self.assertEquals(min(Variable(), 0).sign, u.Sign.NEGATIVE)
        self.assertEquals(min(Variable(), Variable()).sign, u.Sign.UNKNOWN)
        self.assertEquals(min(Variable(), -2).sign, u.Sign.NEGATIVE)

        self.assertEquals(min(0, 0).sign, u.Sign.ZERO)
        self.assertEquals(min(0, -2).sign, u.Sign.NEGATIVE)

        self.assertEquals(min(-3, -2).sign, u.Sign.NEGATIVE)

        # Many args.
        self.assertEquals(min(-2, Variable(), 0, -1, Variable(), 1).sign,
                          u.Sign.NEGATIVE)

    # Test the vstack class.
    def test_vstack(self):
        atom = vstack(self.x, self.y, self.x)
        self.assertEquals(atom.name(), "vstack(x, y, x)")
        self.assertEquals(atom.size, (6,1))

        atom = vstack(self.A, self.C, self.B)
        self.assertEquals(atom.name(), "vstack(A, C, B)")
        self.assertEquals(atom.size, (7,2))

        gen = (xi for xi in self.x)
        atom = vstack(*gen)
        # self.assertEqual(atom[1,0].name(), "vstack(x[0,0], x[1,0])[1,0]")

        with self.assertRaises(Exception) as cm:
            vstack(self.C, 1)
        self.assertEqual(str(cm.exception),
            "All arguments to vstack must have the same number of columns.")

        with self.assertRaises(Exception) as cm:
            vstack()
        self.assertEqual(str(cm.exception),
            "No arguments given to 'vstack'.")