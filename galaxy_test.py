import unittest
import galaxy as g

class GalaxyTests(unittest.TestCase):

    def test_rand_type_initial_type_ratio_0(self):
        # Test rand_type with initial_type_ratio = 0
        # The result should always be 'spiral'

        initial_type_ratio = 0
        num_tests = 50

        for _ in range(num_tests):
            galaxy_type = g.rand_type(initial_type_ratio)
            self.assertEqual(galaxy_type, 'spiral')

    def test_rand_type_initial_type_ratio_1(self):
        # Test rand_type with initial_type_ratio = 1
        # The result should always be 'elliptical'

        initial_type_ratio = 1
        num_tests = 50

        for _ in range(num_tests):
            galaxy_type = g.rand_type(initial_type_ratio)
            self.assertEqual(galaxy_type, 'elliptical')

    def test_rand_type(self):
        # Test the rand_type function
        # Check if the returned galaxy type is either 'elliptical' or 'spiral'

        # Test case 1: initial_type_ratio = 0.0
        galaxy_type = g.rand_type(0.0)
        self.assertIn(galaxy_type, ['elliptical', 'spiral'])

        # Test case 2: initial_type_ratio = 1.0
        galaxy_type = g.rand_type(1.0)
        self.assertIn(galaxy_type, ['elliptical', 'spiral'])

        # Test case 3: initial_type_ratio = 0.5
        galaxy_type = g.rand_type(0.5)
        self.assertIn(galaxy_type, ['elliptical', 'spiral'])

    def test_gravity_force(self):
        # Test the gravity_force function
        # Check if the returned force components are floats

        galaxy_one = g.Galaxy(1, 0, 0, 100, 'elliptical')
        galaxy_two = g.Galaxy(2, 3, 4, 200, 'spiral')
        force_x, force_y = g.gravity_force(galaxy_one, galaxy_two)

        self.assertIsInstance(force_x, float)
        self.assertIsInstance(force_y, float)

    def test_elliptical_ratio(self):
        # Test the elliptical_ratio function
        # Check if the returned ratio is within the range [0, 1]

        galaxy_list = [
            g.Galaxy(1, 0, 0, 100, 'elliptical'),
            g.Galaxy(2, 1, 1, 200, 'spiral'),
            g.Galaxy(3, 2, 2, 300, 'elliptical')
        ]
        universe_size = 1000

        ratio = g.elliptical_ratio(galaxy_list)

        self.assertGreaterEqual(ratio, 0)
        self.assertLessEqual(ratio, 1)

    def test_elliptical_ratio_example(self):
        # Test elliptical_ratio function

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

if __name__ == '__main__':
    unittest.main()
