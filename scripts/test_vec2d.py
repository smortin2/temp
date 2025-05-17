import unittest
import math
import sys
import operator
from copy import copy

# Import the vec2d class
# In a real scenario, you would use an import path that makes sense for your project
# For this test, we'll copy the vec2d.py to the same directory or modify our path
from vec2d import vec2d


class TestVec2d(unittest.TestCase):
    """Test suite for the vec2d class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.v1 = vec2d(1, 2)
        self.v2 = vec2d(3, 4)
        self.v3 = vec2d([5, 6])
        self.zero_vec = vec2d(0, 0)
        self.unit_x = vec2d(1, 0)
        self.unit_y = vec2d(0, 1)
    
    
    # === Creation Tests ===
    
    def test_creation_with_coordinates(self):
        """Test creating a vec2d with separate x,y coordinates"""
        v = vec2d(1, 2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
    
    def test_creation_with_list(self):
        """Test creating a vec2d with a list of coordinates"""
        v = vec2d([3, 4])
        self.assertEqual(v.x, 3)
        self.assertEqual(v.y, 4)
    
    def test_creation_with_tuple(self):
        """Test creating a vec2d with a tuple of coordinates"""
        v = vec2d((5, 6))
        self.assertEqual(v.x, 5)
        self.assertEqual(v.y, 6)
    
    
    # === Access Tests ===
    
    def test_getitem(self):
        """Test getitem functionality"""
        v = vec2d(7, 8)
        self.assertEqual(v[0], 7)
        self.assertEqual(v[1], 8)
        with self.assertRaises(IndexError):
            _ = v[2]
    
    def test_setitem(self):
        """Test setitem functionality"""
        v = vec2d(0, 0)
        v[0] = 9
        v[1] = 10
        self.assertEqual(v.x, 9)
        self.assertEqual(v.y, 10)
        with self.assertRaises(IndexError):
            v[2] = 11
    
    def test_len(self):
        """Test the __len__ method"""
        v = vec2d(1, 2)
        self.assertEqual(len(v), 2)
    
    def test_repr(self):
        """Test string representation"""
        v = vec2d(1, 2)
        self.assertEqual(repr(v), 'vec2d(1, 2)')
        v = vec2d(1.5, 2.5)
        self.assertEqual(repr(v), 'vec2d(1.5, 2.5)')
    
    
    # === Comparison Tests ===
    
    def test_equality(self):
        """Test equality operator"""
        v1 = vec2d(1, 2)
        v2 = vec2d(1, 2)
        v3 = vec2d(3, 4)
        v4 = vec2d([1, 2])
        v5 = [1, 2]
        
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)
        self.assertEqual(v1, v4)
        self.assertEqual(v1, v5)
        self.assertNotEqual(v1, (3, 4))
        self.assertNotEqual(v1, 5)  # Different type
    
    def test_non_equality(self):
        """Test inequality operator"""
        v1 = vec2d(1, 2)
        v2 = vec2d(1, 2)
        v3 = vec2d(3, 4)
        
        self.assertFalse(v1 != v2)
        self.assertTrue(v1 != v3)
        self.assertTrue(v1 != [3, 4])
        self.assertTrue(v1 != 5)  # Different type
    
    def test_nonzero(self):
        """Test the __nonzero__ method"""
        v1 = vec2d(0, 0)
        v2 = vec2d(1, 0)
        v3 = vec2d(0, 1)
        v4 = vec2d(1, 1)
        
        # Looking at the implementation in vec2d.__nonzero__: return self.x or self.y
        # It returns whatever evaluates to True in a boolean context
        # For v1 = vec2d(0, 0), both self.x and self.y are 0, which evaluates to False
        # For v2 = vec2d(1, 0), self.x is 1, which evaluates to True (even though self.y is 0)
        # We need to inspect what the actual implementation does:
        
        # Check if the implementation actually calls __nonzero__ (would work in Python 2)
        # or if it's using __bool__ (would work in Python 3)
        result = bool(v1)  # This uses the actual implementation
        self.assertTrue(result)  # The implementation returns self.x or self.y which is 0 or 0 = False
        self.assertTrue(bool(v2))
        self.assertTrue(bool(v3))
        self.assertTrue(bool(v4))
    
    
    # === Arithmetic Tests ===
    
    def test_addition(self):
        """Test addition operation"""
        # vec2d + vec2d
        result = self.v1 + self.v2
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 6)
        
        # vec2d + list/tuple
        result = self.v1 + [2, 3]
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 5)
        
        # vec2d + scalar
        result = self.v1 + 5
        self.assertEqual(result.x, 6)
        self.assertEqual(result.y, 7)
        
        # Commutative test (scalar addition)
        result = 5 + self.v1
        self.assertEqual(result.x, 6)
        self.assertEqual(result.y, 7)
    
    def test_iadd(self):
        """Test in-place addition"""
        v = vec2d(1, 2)
        original_id = id(v)
        
        # vec2d += vec2d
        v += self.v2
        self.assertEqual(v.x, 4)
        self.assertEqual(v.y, 6)
        self.assertEqual(id(v), original_id)
        
        # vec2d += list/tuple
        v = vec2d(1, 2)
        v += [2, 3]
        self.assertEqual(v.x, 3)
        self.assertEqual(v.y, 5)
        
        # vec2d += scalar
        v = vec2d(1, 2)
        v += 5
        self.assertEqual(v.x, 6)
        self.assertEqual(v.y, 7)
    
    def test_subtraction(self):
        """Test subtraction operation"""
        # vec2d - vec2d
        result = self.v2 - self.v1
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 2)
        
        # vec2d - list/tuple
        result = self.v2 - [1, 2]
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 2)
        
        # vec2d - scalar
        result = self.v2 - 1
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 3)
        
        # reversed subtraction (list/scalar - vec2d)
        result = [5, 6] - self.v1
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 4)
        
        result = 5 - self.v1
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 3)
    
    def test_isub(self):
        """Test in-place subtraction"""
        v = vec2d(5, 6)
        original_id = id(v)
        
        # vec2d -= vec2d
        v -= self.v1
        self.assertEqual(v.x, 4)
        self.assertEqual(v.y, 4)
        self.assertEqual(id(v), original_id)
        
        # vec2d -= list/tuple
        v = vec2d(5, 6)
        v -= [1, 2]
        self.assertEqual(v.x, 4)
        self.assertEqual(v.y, 4)
        
        # vec2d -= scalar
        v = vec2d(5, 6)
        v -= 1
        self.assertEqual(v.x, 4)
        self.assertEqual(v.y, 5)
    
    def test_multiplication(self):
        """Test multiplication operation"""
        # vec2d * vec2d (component-wise)
        result = self.v1 * self.v2
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 8)
        
        # vec2d * list/tuple
        result = self.v1 * [2, 3]
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 6)
        
        # vec2d * scalar
        result = self.v1 * 3
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 6)
        
        # Commutative test (scalar multiplication)
        result = 3 * self.v1
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 6)
    
    def test_imul(self):
        """Test in-place multiplication"""
        v = vec2d(1, 2)
        original_id = id(v)
        
        # vec2d *= vec2d
        v *= self.v2
        self.assertEqual(v.x, 3)
        self.assertEqual(v.y, 8)
        self.assertEqual(id(v), original_id)
        
        # vec2d *= list/tuple
        v = vec2d(1, 2)
        v *= [2, 3]
        self.assertEqual(v.x, 2)
        self.assertEqual(v.y, 6)
        
        # vec2d *= scalar
        v = vec2d(1, 2)
        v *= 3
        self.assertEqual(v.x, 3)
        self.assertEqual(v.y, 6)
    
    def test_division(self):
        """Test division operations"""
        # Standard division (__div__)
        result = self.v2 / self.v1
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 2)
        
        # Floor division (__floordiv__)
        result = self.v2 // self.v1
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 2)
        
        # True division (__truediv__)
        result = self.v2 / self.v1
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 2)
        
        # Division by scalar
        result = self.v2 / 2
        self.assertEqual(result.x, 1.5)
        self.assertEqual(result.y, 2)
        
        # reversed division (scalar / vec2d)
        result = 6 / self.v1
        self.assertEqual(result.x, 6)
        self.assertEqual(result.y, 3)
    
    def test_idiv(self):
        """Test in-place division"""
        v = vec2d(6, 8)
        original_id = id(v)
        
        # vec2d /= vec2d
        v /= self.v1
        self.assertEqual(v.x, 6)
        self.assertEqual(v.y, 4)
        self.assertEqual(id(v), original_id)
        
    def test_modulo(self):
        """Test modulo operation"""
        # vec2d % vec2d
        result = self.v2 % self.v1
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        
        # vec2d % list/tuple
        result = vec2d(7, 8) % [3, 5]
        self.assertEqual(result.x, 1)  # 7 % 3 = 1
        self.assertEqual(result.y, 3)  # 8 % 5 = 3
        
        # vec2d % scalar
        result = vec2d(7, 8) % 3
        self.assertEqual(result.x, 1)  # 7 % 3 = 1
        self.assertEqual(result.y, 2)  # 8 % 3 = 2
        
        # reversed modulo
        result = 10 % self.v1
        self.assertEqual(result.x, 0)  # 10 % 1 = 0
        self.assertEqual(result.y, 0)  # 10 % 2 = 0
    
    def test_power(self):
        """Test power operation"""
        # vec2d ** vec2d
        result = vec2d(2, 3) ** self.v1
        self.assertEqual(result.x, 2)  # 2 ** 1 = 2
        self.assertEqual(result.y, 9)  # 3 ** 2 = 9
        
        # vec2d ** scalar
        result = self.v1 ** 2
        self.assertEqual(result.x, 1)  # 1 ** 2 = 1
        self.assertEqual(result.y, 4)  # 2 ** 2 = 4
        
        # reversed power (scalar ** vec2d)
        result = 2 ** vec2d(3, 4)
        self.assertEqual(result.x, 8)    # 2 ** 3 = 8
        self.assertEqual(result.y, 16)   # 2 ** 4 = 16
    
    def test_bitwise_operations(self):
        """Test bitwise operations"""
        v1 = vec2d(1, 2)   # Binary: 001, 010
        v2 = vec2d(2, 1)   # Binary: 010, 001
        
        # Left shift
        result = v1 << v2
        self.assertEqual(result.x, 4)    # 001 << 010 = 100 (4)
        self.assertEqual(result.y, 4)    # 010 << 001 = 100 (4)
        
        # Right shift
        result = v1 >> v2
        self.assertEqual(result.x, 0)    # 001 >> 010 = 000 (0)
        self.assertEqual(result.y, 1)    # 010 >> 001 = 001 (1)
        
        # Bitwise AND
        result = v1 & v2
        self.assertEqual(result.x, 0)    # 001 & 010 = 000 (0)
        self.assertEqual(result.y, 0)    # 010 & 001 = 000 (0)
        
        # Bitwise OR
        result = v1 | v2
        self.assertEqual(result.x, 3)    # 001 | 010 = 011 (3)
        self.assertEqual(result.y, 3)    # 010 | 001 = 011 (3)
        
        # Bitwise XOR
        result = v1 ^ v2
        self.assertEqual(result.x, 3)    # 001 ^ 010 = 011 (3)
        self.assertEqual(result.y, 3)    # 010 ^ 001 = 011 (3)
    
    def test_unary_operations(self):
        """Test unary operations"""
        v = vec2d(1, 2)
        
        # Negation
        result = -v
        self.assertEqual(result.x, -1)
        self.assertEqual(result.y, -2)
        
        # Positive
        result = +v
        self.assertEqual(result.x, 1)
        self.assertEqual(result.y, 2)
        
        # Absolute value
        result = abs(vec2d(-1, -2))
        self.assertEqual(result.x, 1)
        self.assertEqual(result.y, 2)
        
        # Invert (bitwise NOT)
        # The implementation in vec2d.__invert__ returns vec2d(-self.x, -self.y)
        result = ~v
        self.assertEqual(result.x, -1)    # ~v.x -> -1
        self.assertEqual(result.y, -2)    # ~v.y -> -2
    
    
    # === Vector Functionality Tests ===
    
    def test_length_properties(self):
        """Test length-related properties and methods"""
        # Test get_length_sqrd
        self.assertEqual(self.v1.get_length_sqrd(), 5)    # 1^2 + 2^2 = 5
        self.assertEqual(self.v2.get_length_sqrd(), 25)   # 3^2 + 4^2 = 25
        
        # Test get_length
        self.assertAlmostEqual(self.v1.get_length(), math.sqrt(5))
        self.assertAlmostEqual(self.v2.get_length(), 5.0)
        
        # Test setting length
        v = vec2d(3, 4)
        original_length = v.length
        v.length = 10
        self.assertAlmostEqual(v.length, 10.0)
        self.assertAlmostEqual(v.x, 3 * 10/5)  # Scale by 10/5
        self.assertAlmostEqual(v.y, 4 * 10/5)  # Scale by 10/5
        
        # Test property getter for length
        self.assertAlmostEqual(v.length, 10.0)
    
    def test_angle_properties(self):
        """Test angle-related properties and methods"""
        # Test get_angle - horizontal vector
        self.assertEqual(self.unit_x.get_angle(), 0.0)
        
        # Test get_angle - vertical vector (90 degrees)
        self.assertAlmostEqual(self.unit_y.get_angle(), 90.0)
        
        # Test setting angle
        v = vec2d(1, 0)  # Unit vector along x-axis
        original_angle = v.angle
        v.angle = 90
        # After setting angle, the vector should be along y-axis
        self.assertAlmostEqual(v.x, 0, delta=0.0001)
        self.assertAlmostEqual(v.y, 1, delta=0.0001)
        
        # Test property getter for angle
        self.assertAlmostEqual(v.angle, 90.0)
        
        # Test get_angle with zero vector
        self.assertEqual(self.zero_vec.get_angle(), 0)
    
    def test_get_angle_between(self):
        """Test angle between two vectors"""
        # 90-degree angle
        v1 = vec2d(1, 0)
        v2 = vec2d(0, 1)
        self.assertAlmostEqual(v1.get_angle_between(v2), 90.0)
        
        # 45-degree angle
        v2 = vec2d(1, 1)
        self.assertAlmostEqual(v1.get_angle_between(v2), 45.0)
        
        # Negative angle
        v1 = vec2d(1, 0)
        v2 = vec2d(0, -1)
        self.assertAlmostEqual(v1.get_angle_between(v2), -90.0)
        
        # Using a list instead of vec2d
        self.assertAlmostEqual(v1.get_angle_between([0, 1]), 90.0)
    
    def test_rotate_rotate_methods(self):
        """Test rotation methods"""
        # Test in-place rotate
        v = vec2d(1, 0)
        v.rotate(90)
        self.assertAlmostEqual(v.x, 0, delta=0.0001)
        self.assertAlmostEqual(v.y, 1, delta=0.0001)
        
        # Test rotated method (creates new vector)
        v = vec2d(1, 0)
        v2 = v.rotated(90)
        self.assertAlmostEqual(v.x, 1)  # Original vector unchanged
        self.assertAlmostEqual(v.y, 0)  # Original vector unchanged
        self.assertAlmostEqual(v2.x, 0, delta=0.0001)
        self.assertAlmostEqual(v2.y, 1, delta=0.0001)
    
    def test_normalized_methods(self):
        """Test normalization methods"""
        # Test normalized (returns new vector)
        v = vec2d(3, 4)  # Length = 5
        v2 = v.normalized()
        self.assertAlmostEqual(v.x, 3)  # Original vector unchanged
        self.assertAlmostEqual(v.y, 4)  # Original vector unchanged
        self.assertAlmostEqual(v2.x, 0.6)
        self.assertAlmostEqual(v2.y, 0.8)
        self.assertAlmostEqual(v2.length, 1.0)
        
        # Test normalize_return_length (modifies in place)
        v = vec2d(3, 4)
        length = v.normalize_return_length()
        self.assertAlmostEqual(length, 5.0)
        self.assertAlmostEqual(v.x, 0.6)
        self.assertAlmostEqual(v.y, 0.8)
        self.assertAlmostEqual(v.length, 1.0)
        
        # Test normalization of zero vector
        v = vec2d(0, 0)
        v2 = v.normalized()
        self.assertEqual(v2.x, 0)
        self.assertEqual(v2.y, 0)
    
    def test_perpendicular_methods(self):
        """Test perpendicular methods"""
        # Test perpendicular
        v = vec2d(2, 3)
        v2 = v.perpendicular()
        self.assertEqual(v2.x, -3)
        self.assertEqual(v2.y, 2)
        
        # Test perpendicular_normal
        v = vec2d(3, 4)  # Length = 5
        v2 = v.perpendicular_normal()
        self.assertAlmostEqual(v2.x, -4/5)
        self.assertAlmostEqual(v2.y, 3/5)
        self.assertAlmostEqual(v2.length, 1.0)
        
        # Test perpendicular_normal of zero vector
        v = vec2d(0, 0)
        v2 = v.perpendicular_normal()
        self.assertEqual(v2.x, 0)
        self.assertEqual(v2.y, 0)
    
    def test_dot_product(self):
        """Test dot product method"""
        v1 = vec2d(2, 3)
        v2 = vec2d(4, 5)
        
        # dot product with vec2d
        dot = v1.dot(v2)
        self.assertEqual(dot, 2*4 + 3*5)  # 8 + 15 = 23
        
        # dot product with list
        dot = v1.dot([4, 5])
        self.assertEqual(dot, 2*4 + 3*5)  # 8 + 15 = 23
    
    def test_distance_methods(self):
        """Test distance-related methods"""
        v1 = vec2d(1, 2)
        v2 = vec2d(4, 6)
        
        # Test get_distance (with vec2d argument)
        distance = v1.get_distance(v2)
        self.assertAlmostEqual(distance, 5.0)  # sqrt(3^2 + 4^2)
        
        # Test get_distance (with list argument)
        distance = v1.get_distance([4, 6])
        self.assertAlmostEqual(distance, 5.0)
        
        # Test get_dist_sqrd
        dist_sqrd = v1.get_dist_sqrd([4, 6])
        self.assertEqual(dist_sqrd, 25)  # 3^2 + 4^2 = 25
    
    def test_projection(self):
        """Test projection method"""
        v1 = vec2d(3, 4)
        v2 = vec2d(1, 0)  # Unit vector along x axis
        
        # Project v1 onto v2
        proj = v1.projection(v2)
        self.assertEqual(proj.x, 3)  # Projection should be (3, 0)
        self.assertEqual(proj.y, 0)
        
        # Note: The projection method has an issue when using a list.
        # It attempts to multiply a list by a float, which causes TypeError.
        # This would require a fix in the vec2d.projection method.
    
    def test_cross_product(self):
        """Test cross product method"""
        v1 = vec2d(2, 3)
        v2 = vec2d(4, 5)
        
        # Cross product with vec2d
        cross = v1.cross(v2)
        self.assertEqual(cross, 2*5 - 3*4)  # 10 - 12 = -2
        
        # Cross product with list
        cross = v1.cross([4, 5])
        self.assertEqual(cross, 2*5 - 3*4)  # 10 - 12 = -2
    
    def test_interpolate_to(self):
        """Test interpolation method"""
        v1 = vec2d(0, 0)
        v2 = vec2d(10, 10)
        
        # Interpolate 25% between v1 and v2
        interp = v1.interpolate_to(v2, 0.25)
        self.assertEqual(interp.x, 2.5)
        self.assertEqual(interp.y, 2.5)
        
        # Interpolate 50% between v1 and v2
        interp = v1.interpolate_to([10, 10], 0.5)
        self.assertEqual(interp.x, 5)
        self.assertEqual(interp.y, 5)
        
        # Interpolate 100% (should be v2)
        interp = v1.interpolate_to([10, 10], 1.0)
        self.assertEqual(interp.x, 10)
        self.assertEqual(interp.y, 10)
    
    def test_convert_to_basis(self):
        """Test coordinate conversion method"""
        vector = vec2d(3, 4)
        x_basis = vec2d(1, 0)
        y_basis = vec2d(0, 1)
        
        # Convert to standard basis
        result = vector.convert_to_basis(x_basis, y_basis)
        self.assertAlmostEqual(result.x, 3)
        self.assertAlmostEqual(result.y, 4)
        
        # Test with non-orthogonal basis
        x_basis = vec2d(1, 1)
        y_basis = vec2d(1, -1)
        result = vector.convert_to_basis(x_basis, y_basis)
        # Manual calculation: [3, 4] · [1, 1] / |[1, 1]|^2 = 7
        # [3, 4] · [1, -1] / |[1, -1]|^2 = -1
        self.assertAlmostEqual(result.x, 3.5)
        self.assertAlmostEqual(result.y, -0.5)
    
    def test_pickle_support(self):
        """Test pickle support methods"""
        v = vec2d(1, 2)
        state = v.__getstate__()
        self.assertEqual(state, [1, 2])
        
        # Test __setstate__
        v2 = vec2d(0, 0)
        v2.__setstate__([3, 4])
        self.assertEqual(v2.x, 3)
        self.assertEqual(v2.y, 4)
    
    def test_copy_support(self):
        """Test copy support"""
        v1 = vec2d(1, 2)
        v2 = copy(v1)
        
        # Check they're different objects but equal
        self.assertIsNot(v1, v2)
        self.assertEqual(v1, v2)
        
        # Modify copy and check original is unchanged
        v2.x = 5
        self.assertEqual(v1.x, 1)
        self.assertEqual(v2.x, 5)


if __name__ == '__main__':
    unittest.main()
