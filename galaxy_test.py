import unittest
import numpy as np
import galaxy as g

class GalaxyTests(unittest.TestCase):
    """Tests for galaxy.py module, including Galaxy class methods and non-affiliated methods."""

    def test_rand_type_initial_type_ratio_0(self):
        """Test rand_type with initial_type_ratio = 0
        The result should always be 'spiral'
        """

        initial_type_ratio = 0
        num_tests = 50

        for _ in range(num_tests):
            galaxy_type = g.rand_type(initial_type_ratio)
            self.assertEqual(galaxy_type, 'spiral')

    def test_rand_type_initial_type_ratio_1(self):
        """Test rand_type with initial_type_ratio = 1
        The result should always be 'elliptical'"""

        initial_type_ratio = 1
        num_tests = 50

        for _ in range(num_tests):
            galaxy_type = g.rand_type(initial_type_ratio)
            self.assertEqual(galaxy_type, 'elliptical')

    def test_rand_type(self):
        """Test the rand_type function
        Check if the returned galaxy type is either 'elliptical' or 'spiral'"""

        #update to repeatedly run the test and compare with desired ratio
        galaxy_type = g.rand_type(0.5)
        self.assertIn(galaxy_type, ['elliptical', 'spiral'])

    def test_gravity_force(self):#add more tests. add G? make dimensionless?
        """Test the gravity_force function
        Check if the returned force components are floats"""

        galaxy_one = g.Galaxy(1, 0, 0, 100, 'elliptical')
        galaxy_two = g.Galaxy(2, 3, 4, 200, 'spiral')
        force_x, force_y = g.gravity_force(galaxy_one, galaxy_two)

        self.assertIsInstance(force_x, float)
        self.assertIsInstance(force_y, float)

    def test_elliptical_ratio(self):
        """Test the elliptical_ratio function
        Check if the returned ratio is within the range [0, 1]"""

        galaxy_list = [
            g.Galaxy(1, 0, 0, 100, 'elliptical'),
            g.Galaxy(2, 1, 1, 200, 'spiral'),
            g.Galaxy(3, 2, 2, 300, 'elliptical')
        ]

        ratio = g.elliptical_ratio(galaxy_list)

        self.assertGreaterEqual(ratio, 0)
        self.assertLessEqual(ratio, 1)

    def test_elliptical_ratio_example(self):#add more tests of dif vals elliptical ratio!!
        """Test elliptical_ratio function with specific example
        Checks only counts active galaxies."""
        #want to also check visibility: negative positions, positive too large positions

        # Create a list of galaxies
        galaxies = [
            g.Galaxy(0, 0, 0, 100, 'elliptical'),
            g.Galaxy(1, 0, 0, 100, 'spiral'),
            g.Galaxy(2, 0, 0, 100, 'elliptical'),
            g.Galaxy(3, 0, 0, 100, 'elliptical'),
            g.Galaxy(4, 0, 0, 100, 'spiral'),
        ]

        # Make one galaxy inactive
        galaxies[1].active = False

        # Calculate the expected elliptical ratio
        expected_ratio = 3 / 4  # 0.75

        # Call the elliptical_ratio function
        ratio = g.elliptical_ratio(galaxies)

        # Check if the calculated ratio matches the expected ratio
        self.assertAlmostEqual(ratio, expected_ratio, places=4)

    def test_distance_x(self):#confirm sign behavior makes sense
        """Tests distance_x function with specific example."""
        galaxy_one = g.Galaxy(0, 0, 0, 10, 'spiral')
        galaxy_two = g.Galaxy(0, 20, 10, 10, 'elliptical')

        x_dist = galaxy_one.distance_x(galaxy_two)

        self.assertEqual(x_dist, 20)

    def test_distance_y(self):#confirm sign behavior makes sense.
        """Tests distance_y function with specific example."""
        galaxy_one = g.Galaxy(0, 0, 0, 10, 'spiral')
        galaxy_two = g.Galaxy(0, 20, 20, 10, 'elliptical')

        y_dist = galaxy_one.distance_y(galaxy_two)

        self.assertEqual(y_dist, 20)

    def test_distance(self):#confirm sign behavior makes sense wrt gravity function.
        """Tests euclidean distance function with specific example (3-4-5 triangle)."""
        galaxy_one = g.Galaxy(0, 3, 0, 10, 'spiral')
        galaxy_two = g.Galaxy(0, 0, 4, 10, 'elliptical')

        dist = galaxy_one.distance(galaxy_two)

        self.assertEqual(dist, 5)

    def test_angle(self):
        """Test angle function in case of desired positive, negative, zero result.
        Uses 3-4-5 triangle."""
        # Test angle function

        # Test case 1: Positive x and y coordinates
        galaxy_one = g.Galaxy(0, 3, 0, 10, 'elliptical')
        galaxy_two = g.Galaxy(0, 0, 4, 10, 'elliptical')
        expected_angle1 = np.deg2rad(53.130102)

        # Call the angle function
        angle1 = galaxy_one.angle(galaxy_two)

        # Check if the calculated angle matches the expected angle
        self.assertAlmostEqual(angle1, expected_angle1, places=4)

        # Test case 2: Negative x and y coordinates
        galaxy_three = g.Galaxy(0, -5, 0, 10, 'elliptical')
        galaxy_four = g.Galaxy(0, 0, -12, 10, 'spiral')
        expected_angle2 = np.deg2rad(-67.380136)

        # Call the angle function
        angle2 = galaxy_three.angle(galaxy_four)

        # Check if the calculated angle matches the expected angle
        self.assertAlmostEqual(angle2, expected_angle2, places=4)

        # Test case 3: Zero x and y coordinates
        galaxy_five = g.Galaxy(0, 0, 0, 10, 'spiral')
        galaxy_six = g.Galaxy(0, 0, 0, 10, 'spiral')
        expected_angle3 = 0

        # Call the angle function
        angle3 = galaxy_five.angle(galaxy_six)

        # Check if the calculated angle matches the expected angle
        self.assertAlmostEqual(angle3, expected_angle3, places=4)

    def test_visible_true(self):
        """Test visible function works when it should be true."""
        galaxy = g.Galaxy(0, 50, 50, 10, 'spiral')
        universe_size = 1000
        is_visible = galaxy.visible(universe_size)

        self.assertTrue(is_visible)

    def test_visible_not_true_negative(self):
        """Test visible function works when it should be false because galaxy position negative."""
        galaxy = g.Galaxy(0, -100, -20, 10, 'spiral')
        universe_size = 1000
        is_visible = galaxy.visible(universe_size)

        self.assertFalse(is_visible)

    def test_visible_not_true_positive(self):
        """Test visible function works when it should be false because galaxy position too big."""
        galaxy = g.Galaxy(0, 1250, 100, 10, 'spiral')
        universe_size = 1000
        is_visible = galaxy.visible(universe_size)

        self.assertFalse(is_visible)

    def test_collide_bools(self):
        """Test collision function appropriately modifies galaxy attributes.
        1. Check appropriate galaxy made inactive.
        2. Check type of new galaxy elliptical."""
        # Test collide function

        # Test case 1: Colliding galaxies
        galaxy1 = g.Galaxy(1, 0, 0, 1, 'spiral')
        galaxy2 = g.Galaxy(2, 1, 1, 1, 'spiral')

        # Call the collide function
        galaxy1.collide(galaxy2)

        # Check if the collided galaxies are no longer active
        self.assertTrue(galaxy1.active)
        self.assertFalse(galaxy2.active)

        # Check the resulting galaxy is elliptical
        self.assertEqual(galaxy1.gal_type, 'elliptical')

    def test_collide_momentum(self):
        """Test collision function obeys conservation of momentum."""
        return

    def test_time_update(self):
        """Test time update function."""
        return

if __name__ == '__main__':
    unittest.main()
