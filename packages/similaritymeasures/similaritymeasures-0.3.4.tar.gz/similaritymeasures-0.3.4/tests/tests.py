import numpy as np
import unittest
import similaritymeasures
from scipy.spatial.distance import cdist

# let's just define some data
x1 = np.linspace(0.0, 1.0, 100)
y1 = np.ones(100)*2
x2 = np.linspace(0.0, 1.0, 50)
y2 = np.ones(50)

np.random.seed(1212121)
curve_a_rand = np.random.random((100, 2))
curve_b_rand = np.random.random((90, 2))

curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

x1 = np.linspace(0.0, 1.0, 100)
y1 = x1
x2 = np.linspace(0.0, 1.0, 50)
y2 = x2+1.0

curve3 = np.array((x1, y1)).T
curve4 = np.array((x2, y2)).T

P = np.array([[0, 0], [1, 1], [2, 2]])
Q = P.copy()
Q[:, 1] = Q[:, 1] + 1

r1 = 10
r2 = 100
theta = np.linspace(0.0, 2.0*np.pi, 100)
x1 = np.cos(theta)*r1
x2 = np.cos(theta)*r2
y1 = np.sin(theta)*r1
y2 = np.sin(theta)*r2
curve5 = np.array((x1, y1)).T
curve6 = np.array((x2, y2)).T


class TestEverything(unittest.TestCase):

    def test_c1_c2_area(self):
        area = similaritymeasures.area_between_two_curves(curve1, curve2)
        self.assertTrue(area, 1.0)

    def test_c1_c2_area_swapped(self):
        area = similaritymeasures.area_between_two_curves(curve2, curve1)
        self.assertTrue(area, 1.0)

    def test_c3_c4_area(self):
        area = similaritymeasures.area_between_two_curves(curve3, curve4)
        self.assertTrue(area, 1.0)

    def test_c1_c2_pcm(self):
        pcm = similaritymeasures.pcm(curve1, curve2)
        self.assertTrue(pcm, np.nan)

    def test_pcm_rev(self):
        x1 = np.linspace(0.0, 1.0, 100)
        y1 = x1*20.0
        temp1 = np.array((x1, y1)).T
        x2 = np.linspace(1.0, 2.5, 50)
        y2 = x2*3.0
        temp2 = np.array((x2, y2)).T
        _ = similaritymeasures.pcm(temp2, temp1)
        self.assertTrue(True)

    def test_c1_c2_pcm_swapped(self):
        pcm = similaritymeasures.pcm(curve2, curve1)
        self.assertTrue(pcm, np.nan)

    def test_c3_c4_pcm(self):
        pcm = similaritymeasures.pcm(curve3, curve4)
        self.assertTrue(pcm, 50.0)

    def test_c1_c2_df(self):
        df = similaritymeasures.frechet_dist(curve1, curve2)
        self.assertTrue(df, 1.0)

    def test_c3_c4_df(self):
        df = similaritymeasures.frechet_dist(curve3, curve4)
        self.assertTrue(df, 1.0)

    def test_c1_c2_cl(self):
        cl = similaritymeasures.curve_length_measure(curve1, curve2)
        self.assertTrue(cl, 4.054651081081643)

    def test_c3_c4_cl(self):
        cl = similaritymeasures.curve_length_measure(curve3, curve4)
        self.assertTrue(cl, 10.986122886681098)

    def test_P_Q_dtw(self):
        r, _ = similaritymeasures.dtw(P, Q)
        self.assertTrue(r, 3.0)

    def test_c5_c6_dtw(self):
        r, _ = similaritymeasures.dtw(curve5, curve6)
        self.assertTrue(np.isclose(r, 9000.0))

    def test_c5_c6_df(self):
        df = similaritymeasures.frechet_dist(curve5, curve6)
        self.assertTrue(np.isclose(df, 90.0))

    def test_P_Q_dtw_path(self):
        r, d = similaritymeasures.dtw(P, Q)
        path = similaritymeasures.dtw_path(d)
        c = cdist(P, Q)
        cost = sum(c[path[:, 0], path[:, 1]])
        self.assertTrue(np.isclose(r, cost))

    def test_c5_c6_dtw_path(self):
        r, d = similaritymeasures.dtw(curve5, curve6)
        path = similaritymeasures.dtw_path(d)
        c = cdist(curve5, curve6)
        cost = sum(c[path[:, 0], path[:, 1]])
        self.assertTrue(np.isclose(r, cost))

    def test_P_Q_dtw_cityblock(self):
        r, _ = similaritymeasures.dtw(P, Q, metric='cityblock')
        self.assertTrue(r, 3.0)

    def test_P_Q_dtw_minkowski_p1(self):
        r, _ = similaritymeasures.dtw(P, Q, metric='minkowski', p=1)
        self.assertTrue(r, 3.0)

    def test_P_Q_dtw_minkowski_p3(self):
        r, _ = similaritymeasures.dtw(P, Q, metric='minkowski', p=3)
        self.assertTrue(r, 3.0)

    def test_complex_quad(self):
        a = [0., 0.]
        b = [1., 1.]
        c = [1., 0.]
        d = [0., 1.]
        quad = similaritymeasures.is_simple_quad(a, b, d, c)
        self.assertFalse(quad)

    def test_random_dtw(self):
        r, d = similaritymeasures.dtw(curve_a_rand, curve_b_rand)
        path = similaritymeasures.dtw_path(d)
        c = cdist(curve_a_rand, curve_b_rand)
        cost = np.sum(c[path[:, 0], path[:, 1]])
        self.assertTrue(np.isclose(r, cost))

    def test_random_pcm(self):
        _ = similaritymeasures.pcm(curve_a_rand, curve_b_rand)
        self.assertTrue(True)

    def test_random_area(self):
        _ = similaritymeasures.area_between_two_curves(curve_a_rand,
                                                       curve_b_rand)
        self.assertTrue(True)

    def test_random_cl(self):
        _ = similaritymeasures.curve_length_measure(curve_a_rand, curve_b_rand)
        self.assertTrue(True)

    def test_random_fr(self):
        _ = similaritymeasures.frechet_dist(curve_a_rand, curve_b_rand)
        self.assertTrue(True)

    def test_cl_zeros(self):
        z1 = np.zeros((100, 2))
        z2 = np.zeros((100, 2))
        _ = similaritymeasures.curve_length_measure(z1, z2)
        self.assertTrue(True)


if __name__ == '__main__':

    unittest.main()
