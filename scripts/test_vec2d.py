import unittest
import math
import sys
import operator
from copy import copy

# Import the vec2d class
# In a real scenario, you would use an import path that makes sense for your project
# For this test, we'll copy the vec2d.py to the same directory or modify our path
sys.path.append('/tmp/extracted/game-master/scripts')
from vec2d import vec2d


class TestVec2d(unittest.TestCase):
	"""Test suite for the vec2d class"""

	def setUp(self):
		"""Set up test fixtures - empty as we're using function scope for vectors"""
		pass

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

	def test_bool(self):
		"""Test the __bool__ method (Python 3's truth value testing)"""
		v1 = vec2d(0, 0)
		v2 = vec2d(1, 0)
		v3 = vec2d(0, 1)
		v4 = vec2d(1, 1)
		v5 = vec2d(0.001, 0)

		# In Python 3, a vector should be False only if it has no magnitude
		# i.e., if both x and y are 0
		self.assertFalse(bool(v1), "Zero vector should be False")
		self.assertTrue(bool(v2), "Vector with x!=0 should be True")
		self.assertTrue(bool(v3), "Vector with y!=0 should be True")
		self.assertTrue(bool(v4), "Vector with both components non-zero should be True")
		self.assertTrue(bool(v5), "Vector with very small magnitude should still be True")

	# === Arithmetic Tests ===

	def test_addition(self):
		"""Test addition operation"""
		# vec2d + vec2d
		result = vec2d(1, 2) + vec2d(3, 4)
		self.assertEqual(result.x, 4)
		self.assertEqual(result.y, 6)

		# vec2d + list/tuple
		result = vec2d(1, 2) + [2, 3]
		self.assertEqual(result.x, 3)
		self.assertEqual(result.y, 5)

		# vec2d + scalar
		result = vec2d(1, 2) + 5
		self.assertEqual(result.x, 6)
		self.assertEqual(result.y, 7)

		# Commutative test (scalar addition)
		result = 5 + vec2d(1, 2)
		self.assertEqual(result.x, 6)
		self.assertEqual(result.y, 7)

	def test_iadd(self):
		"""Test in-place addition"""
		# Test in-place vs out of place with vec2d
		v1 = vec2d(1, 2)
		v2 = vec2d(3, 4)

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 += v2
		v4 = v1 + v2

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)  # Check it's truly in-place

		# Test in-place vs out of place with list/tuple
		v1 = vec2d(1, 2)
		test_list = [2, 3]

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 += test_list
		v4 = v1 + test_list

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

		# Test in-place vs out of place with scalar
		v1 = vec2d(1, 2)
		scalar = 5

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 += scalar
		v4 = v1 + scalar

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

	def test_subtraction(self):
		"""Test subtraction operation"""
		# vec2d - vec2d
		result = vec2d(3, 4) - vec2d(1, 2)
		self.assertEqual(result.x, 2)
		self.assertEqual(result.y, 2)

		# vec2d - list/tuple
		result = vec2d(3, 4) - [1, 2]
		self.assertEqual(result.x, 2)
		self.assertEqual(result.y, 2)

		# vec2d - scalar
		result = vec2d(3, 4) - 1
		self.assertEqual(result.x, 2)
		self.assertEqual(result.y, 3)

		# reversed subtraction (list/scalar - vec2d)
		result = [5, 6] - vec2d(1, 2)
		self.assertEqual(result.x, 4)
		self.assertEqual(result.y, 4)

		result = 5 - vec2d(1, 2)
		self.assertEqual(result.x, 4)
		self.assertEqual(result.y, 3)

	def test_isub(self):
		"""Test in-place - operation"""
		# Test in-place vs out of place with vec2d
		v1 = vec2d(1, 2)
		v2 = vec2d(3, 4)

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 -= v2
		v4 = v1 - v2

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)  # Check it's truly in-place

		# Test in-place vs out of place with list/tuple
		v1 = vec2d(1, 2)
		test_list = [2, 3]

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 -= test_list
		v4 = v1 - test_list

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

		# Test in-place vs out of place with scalar
		v1 = vec2d(1, 2)
		scalar = 3

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 -= scalar
		v4 = v1 - scalar

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

	def test_multiplication(self):
		"""Test multiplication operation"""
		# vec2d * vec2d (component-wise)
		result = vec2d(1, 2) * vec2d(3, 4)
		self.assertEqual(result.x, 3)
		self.assertEqual(result.y, 8)

		# vec2d * list/tuple
		result = vec2d(1, 2) * [2, 3]
		self.assertEqual(result.x, 2)
		self.assertEqual(result.y, 6)

		# vec2d * scalar
		result = vec2d(1, 2) * 3
		self.assertEqual(result.x, 3)
		self.assertEqual(result.y, 6)

		# Commutative test (scalar multiplication)
		result = 3 * vec2d(1, 2)
		self.assertEqual(result.x, 3)
		self.assertEqual(result.y, 6)

	def test_imul(self):
		"""Test in-place * operation"""
		# Test in-place vs out of place with vec2d
		v1 = vec2d(1, 2)
		v2 = vec2d(3, 4)

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 *= v2
		v4 = v1 * v2

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)  # Check it's truly in-place

		# Test in-place vs out of place with list/tuple
		v1 = vec2d(1, 2)
		test_list = [2, 3]

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 *= test_list
		v4 = v1 * test_list

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

		# Test in-place vs out of place with scalar
		v1 = vec2d(1, 2)
		scalar = 3

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 *= scalar
		v4 = v1 * scalar

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

	def test_division(self):
		"""Test division operations"""
		# Standard division (__div__)
		result = vec2d(3, 4) / vec2d(1, 2)
		self.assertEqual(result.x, 3)
		self.assertEqual(result.y, 2)

		# Floor division (__floordiv__)
		result = vec2d(3, 4) // vec2d(1, 2)
		self.assertEqual(result.x, 3)
		self.assertEqual(result.y, 2)

		# True division (__truediv__)
		result = vec2d(3, 4) / vec2d(1, 2)
		self.assertEqual(result.x, 3)
		self.assertEqual(result.y, 2)

		# Division by scalar
		result = vec2d(3, 4) / 2
		self.assertEqual(result.x, 1.5)
		self.assertEqual(result.y, 2)

		# reversed division (scalar / vec2d)
		result = 6 / vec2d(1, 2)
		self.assertEqual(result.x, 6)
		self.assertEqual(result.y, 3)

	def test_idiv(self):
		"""Test in-place / operation"""
		# Test in-place vs out of place with vec2d
		v1 = vec2d(1, 2)
		v2 = vec2d(3, 4)

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 /= v2
		v4 = v1 / v2

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)  # Check it's truly in-place

		# Test in-place vs out of place with list/tuple
		v1 = vec2d(1, 2)
		test_list = [2, 3]

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 /= test_list
		v4 = v1 / test_list

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

		# Test in-place vs out of place with scalar
		v1 = vec2d(1, 2)
		scalar = 3

		v3 = vec2d(1, 2)
		v3_id = id(v3)
		v3 /= scalar
		v4 = v1 / scalar

		self.assertEqual(v3, v4)
		self.assertEqual(id(v3), v3_id)

	def test_modulo(self):
		"""Test modulo operation"""
		# vec2d % vec2d
		result = vec2d(7, 11) % vec2d(3, 4)
		self.assertEqual(result.x, 1)  # 7 % 3 = 1
		self.assertEqual(result.y, 3)  # 11 % 4 = 3

		# vec2d % list/tuple
		result = vec2d(13, 17) % [5, 7]
		self.assertEqual(result.x, 3)  # 13 % 5 = 3
		self.assertEqual(result.y, 3)  # 17 % 7 = 3

		# vec2d % scalar
		result = vec2d(11, 13) % 4
		self.assertEqual(result.x, 3)  # 11 % 4 = 3
		self.assertEqual(result.y, 1)  # 13 % 4 = 1

		# reversed modulo (scalar % vec2d)
		result = 17 % vec2d(5, 7)
		self.assertEqual(result.x, 2)  # 17 % 5 = 2
		self.assertEqual(result.y, 3)  # 17 % 7 = 3

	def test_power(self):
		"""Test power operation"""
		# vec2d ** vec2d
		result = vec2d(2, 3) ** vec2d(1, 2)
		self.assertEqual(result.x, 2)  # 2 ** 1 = 2
		self.assertEqual(result.y, 9)  # 3 ** 2 = 9

		# vec2d ** scalar
		result = vec2d(1, 2) ** 2
		self.assertEqual(result.x, 1)  # 1 ** 2 = 1
		self.assertEqual(result.y, 4)  # 2 ** 2 = 4

		# reversed power (scalar ** vec2d)
		result = 2 ** vec2d(3, 4)
		self.assertEqual(result.x, 8)  # 2 ** 3 = 8
		self.assertEqual(result.y, 16)  # 2 ** 4 = 16

	def test_bitwise_operations(self):
		"""Test bitwise operations"""
		v1 = vec2d(1, 2)  # Binary: 001, 010
		v2 = vec2d(2, 1)  # Binary: 010, 001

		# Left shift
		result = v1 << v2
		self.assertEqual(result.x, 4)  # 001 << 010 = 100 (4)
		self.assertEqual(result.y, 4)  # 010 << 001 = 100 (4)

		# Right shift
		result = v1 >> v2
		self.assertEqual(result.x, 0)  # 001 >> 010 = 000 (0)
		self.assertEqual(result.y, 1)  # 010 >> 001 = 001 (1)

		# Bitwise AND
		result = v1 & v2
		self.assertEqual(result.x, 0)  # 001 & 010 = 000 (0)
		self.assertEqual(result.y, 0)  # 010 & 001 = 000 (0)

		# Bitwise OR
		result = v1 | v2
		self.assertEqual(result.x, 3)  # 001 | 010 = 011 (3)
		self.assertEqual(result.y, 3)  # 010 | 001 = 011 (3)

		# Bitwise XOR
		result = v1 ^ v2
		self.assertEqual(result.x, 3)  # 001 ^ 010 = 011 (3)
		self.assertEqual(result.y, 3)  # 010 ^ 001 = 011 (3)

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
		self.assertEqual(result.x, -1)  # ~v.x -> -1
		self.assertEqual(result.y, -2)  # ~v.y -> -2

	# === Vector Functionality Tests ===

	def test_length_properties(self):
		"""Test length-related properties and methods"""
		# Test get_length_sqrd
		v1 = vec2d(1, 2)
		v2 = vec2d(3, 4)

		self.assertEqual(v1.get_length_sqrd(), 5)  # 1^2 + 2^2 = 5
		self.assertEqual(v2.get_length_sqrd(), 25)  # 3^2 + 4^2 = 25

		# Test get_length
		self.assertAlmostEqual(v1.get_length(), math.sqrt(5))
		self.assertAlmostEqual(v2.get_length(), 5.0)

		# Test setting length
		v = vec2d(3, 4)  # Length is 5
		v.length = 10
		self.assertAlmostEqual(v.x, 6)  # 3 * (10/5)
		self.assertAlmostEqual(v.y, 8)  # 4 * (10/5)
		self.assertAlmostEqual(v.length, 10.0)

		# Test setting length of non-unit vectors at various angles
		v = vec2d(2, 2)  # 45 degree angle, length ≈ 2.8284
		v.length = 4
		self.assertAlmostEqual(v.x, 2.8284, places=4)
		self.assertAlmostEqual(v.y, 2.8284, places=4)
		self.assertAlmostEqual(v.length, 4.0)

		# Test setting length of zero vector (edge case)
		v = vec2d(0, 0)
		with self.assertRaises(ZeroDivisionError):
			v.length = 5  # Cannot set length of zero vector due to undefined direction

		# Test setting length to zero (edge case)
		v = vec2d(3, 4)
		expected_v = vec2d(0, 0)
		v.length = 0
		self.assertEqual(v, expected_v)

	def test_angle_properties(self):
		"""Test angle-related properties and methods"""
		test_angles = [0, 45, 90, 120, 180, -45, -90, -120, -180]

		# Test unit vectors at different angles
		for angle in test_angles:
			# Create vector with specified angle
			v = vec2d(1, 0)
			v.angle = angle

			# Verify angle is normalized to [-180, 180] range
			expected_angle = angle
			while expected_angle <= -180:
				expected_angle += 360
			while expected_angle > 180:
				expected_angle -= 360

			self.assertAlmostEqual(v.angle, expected_angle, places=5,
								   msg=f"Angle getter failed for {angle} degrees")

			# Verify components based on angle
			expected_x = math.cos(math.radians(angle))
			expected_y = math.sin(math.radians(angle))
			self.assertAlmostEqual(v.x, expected_x, places=5,
								   msg=f"x-component incorrect for {angle} degrees")
			self.assertAlmostEqual(v.y, expected_y, places=5,
								   msg=f"y-component incorrect for {angle} degrees")

		# Test angle of vectors with different magnitudes
		v = vec2d(3, 3)  # 45 degrees, magnitude = 3√2
		self.assertAlmostEqual(v.angle, 45.0)

		v = vec2d(-2, 2)  # 135 degrees, magnitude = 2√2
		self.assertAlmostEqual(v.angle, 135.0)

		# Test get_angle with zero vector (should return 0)
		v = vec2d(0, 0)
		self.assertEqual(v.get_angle(), 0)

		# Test setting angle for vectors of different magnitudes
		v = vec2d(3, 4)  # magnitude = 5
		orig_length = v.length
		v.angle = 60
		self.assertAlmostEqual(v.length, orig_length)  # Length should be preserved
		self.assertAlmostEqual(v.x, 5 * math.cos(math.radians(60)))
		self.assertAlmostEqual(v.y, 5 * math.sin(math.radians(60)))

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
		self.assertAlmostEqual(v2.x, -4 / 5)
		self.assertAlmostEqual(v2.y, 3 / 5)
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
		self.assertEqual(dot, 2 * 4 + 3 * 5)  # 8 + 15 = 23

		# dot product with list
		dot = v1.dot([4, 5])
		self.assertEqual(dot, 2 * 4 + 3 * 5)  # 8 + 15 = 23

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

		# Project onto non-unit vectors
		v3 = vec2d(2, 2)  # 45-degree vector
		proj = v1.projection(v3)
		self.assertAlmostEqual(proj.x, 3.5)  # (3*2 + 4*2)/(8)*2 = 3.5
		self.assertAlmostEqual(proj.y, 3.5)  # Same as x for 45-degree vector

		# Project onto vertical vector
		v4 = vec2d(0, 1)
		proj = v1.projection(v4)
		self.assertAlmostEqual(proj.x, 0)
		self.assertAlmostEqual(proj.y, 4)

		# Test with list
		try:
			proj = v1.projection([1, 0])
			self.assertEqual(proj.x, 3)
			self.assertEqual(proj.y, 0)
		except Exception as e:
			self.fail(f"projection() should accept a list as input, but raised an exception: {e}")

		# Project zero vector
		v5 = vec2d(0, 0)
		proj = v5.projection(v2)
		self.assertEqual(proj.x, 0)
		self.assertEqual(proj.y, 0)

		# Project onto zero vector (should raise ZeroDivisionError)
		with self.assertRaises(ZeroDivisionError):
			proj = v1.projection(v5)

	def test_cross_product(self):
		"""Test cross product method"""
		v1 = vec2d(2, 3)
		v2 = vec2d(4, 5)

		# Cross product with vec2d
		cross = v1.cross(v2)
		self.assertEqual(cross, 2 * 5 - 3 * 4)  # 10 - 12 = -2

		# Cross product with list
		cross = v1.cross([4, 5])
		self.assertEqual(cross, 2 * 5 - 3 * 4)  # 10 - 12 = -2

	def test_interpolate_to(self):
		"""Test interpolation method"""
		v1 = vec2d(0, 0)
		v2 = vec2d(10, 10)

		# Test interpolation with vec2d
		self.assertEqual(v1.interpolate_to(v2, 0.5), vec2d(5, 5))

		# Test interpolation with list
		self.assertEqual(v1.interpolate_to([10, 10], 0.0), v1)
		self.assertEqual(v1.interpolate_to([10, 10], 1.0), v2)

		# Test interpolation beyond bounds (extrapolation)
		result = v1.interpolate_to(v2, 1.5)
		self.assertEqual(result.x, 15)
		self.assertEqual(result.y, 15)

		# Test with unequal x,y changes
		v3 = vec2d(-1, 1)
		result = v1.interpolate_to(v3, 0.5)
		self.assertEqual(result.x, -0.5)
		self.assertEqual(result.y, 0.5)

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
		"""Test pickle support"""
		import pickle

		# Test the low-level pickle support methods
		v = vec2d(1, 2)
		state = v.__getstate__()
		self.assertEqual(state, [1, 2])

		v2 = vec2d(0, 0)
		v2.__setstate__([3, 4])
		self.assertEqual(v2.x, 3)
		self.assertEqual(v2.y, 4)

		# Test actual pickling functionality
		original = vec2d(5, 6)
		data = pickle.dumps(original)
		restored = pickle.loads(data)

		# Check if the restored vector is equal to original
		self.assertEqual(restored, original)
		self.assertEqual(restored.x, 5)
		self.assertEqual(restored.y, 6)

		# Test pickling of more complex vectors
		vectors = [
			vec2d(1.5, -2.7),  # Floating point
			vec2d(0, 0),  # Zero vector
			vec2d(-10, 10),  # Integer opposite signs
		]

		for v in vectors:
			restored = pickle.loads(pickle.dumps(v))
			self.assertEqual(restored, v)
			self.assertAlmostEqual(restored.x, v.x)
			self.assertAlmostEqual(restored.y, v.y)

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
