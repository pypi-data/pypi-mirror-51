import unittest
from scipy.stats import norm
import warnings
import pickle
import tensorflow as tf
import sys
import os
import numpy as np
import scipy.stats as stats

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cde.utils.center_point_select import sample_center_points
from cde.utils.misc import norm_along_axis_1
from cde.utils.integration import mc_integration_student_t, numeric_integation
from cde.utils.async_executor import execute_batch_async_pdf
from cde.utils.distribution import batched_univ_t_pdf, batched_univ_t_cdf, batched_univ_t_rvs


class TestHelpers(unittest.TestCase):

  """ sample center points """

  def test_1_shape_center_point(self):
    methods = ["all", "random", "k_means" , "agglomerative", "distance"]
    for m in methods:
      Y = np.random.uniform(size=(120,2))
      centers = sample_center_points(Y, method=m, k=50)
      self.assertEqual(centers.ndim, Y.ndim)
      self.assertEqual(centers.shape[1], Y.shape[1])

  def test_1_center_point_k_means(self):
    Y = np.asarray([1.0, 2.0])
    centers = sample_center_points(Y, method="k_means", k=1)
    self.assertAlmostEqual(Y.mean(), centers.mean())

  def test_1_center_point_agglomerative(self):
    Y = np.random.uniform(size=[20,3])
    centers = sample_center_points(Y, method="agglomerative", k=1)
    self.assertAlmostEqual(Y.mean(), centers.mean())

  def test_1_shape_center_point_distance(self):
    Y = np.asarray([1.0, 1.2, 1.7, 1.9, 2.0])
    centers = sample_center_points(Y, method="distance", k=2)
    self.assertAlmostEqual(centers.mean(), 1.5)

    Y = np.asarray([1.0, 1.2, 1.5, 1.7, 1.9, 2.0])
    centers = sample_center_points(Y, method="distance", k=3)
    self.assertAlmostEqual(centers.mean(), 1.5)

    Y = np.asarray(list(reversed([1.0, 1.2, 1.7, 1.9, 2.0])))
    centers = sample_center_points(Y, method="distance", k=2)
    self.assertAlmostEqual(centers.mean(), 1.5)

  def test_1_shape_center_point_keep_edges(self):
    methods = ["random", "k_means", "agglomerative"]
    for m in methods:
      Y = np.random.uniform(size=(100,2))
      centers = sample_center_points(Y, method=m, k=5, keep_edges=True)
      self.assertEqual(centers.ndim, Y.ndim)
      self.assertEqual(centers.shape[1], Y.shape[1])

  """ norm along axis """

  def test_2_norm_along_axis_1(self):
    A = np.asarray([[1.0, 0.0], [1.0, 0.0]])
    B = np.asarray([[0.0,0.0], [0.0,0.0]])
    dist1 = norm_along_axis_1(A, B, squared=True)
    dist2 = norm_along_axis_1(A, B, squared=False)
    self.assertEqual(np.mean(dist1), 1.0)
    self.assertEqual(np.mean(dist2), 1.0)

  def test_2_norm_along_axis_2(self):
    A = np.asarray([[1.0, 0.0]])
    B = np.asarray([[0.0,0.0]])
    dist1 = norm_along_axis_1(A, B, squared=True)
    dist2 = norm_along_axis_1(A, B, squared=False)
    self.assertEqual(np.mean(dist1), 1.0)
    self.assertEqual(np.mean(dist2), 1.0)

  def test_2_norm_along_axis_3(self):
    A = np.random.uniform(size=[20, 3])
    B = np.random.uniform(size=[10, 3])
    dist = norm_along_axis_1(A, B, squared=True)
    self.assertEqual(dist.shape, (20,10))

  """ monte carlo integration """

  def test_mc_integration_t_1(self):
    func = lambda y: np.expand_dims(stats.multivariate_normal.pdf(y, mean=[0, 0], cov=np.diag([2, 2])), axis=1)
    integral = mc_integration_student_t(func, ndim=2, n_samples=10 ** 7, batch_size=10 ** 6)
    self.assertAlmostEqual(1.0, integral[0], places=2)

  def test_mc_integration_t_2(self):
    func = lambda y: y * np.tile(np.expand_dims(stats.multivariate_normal.pdf(y, mean=[1, 2], cov=np.diag([2, 2])), axis=1), (1,2))
    integral = mc_integration_student_t(func, ndim=2, n_samples=10 ** 7, batch_size=10 ** 6)
    self.assertAlmostEqual(1, integral[0], places=2)
    self.assertAlmostEqual(2, integral[1], places=2)

class TestExecAsyncBatch(unittest.TestCase):

  def test_batch_exec_1(self):
    def pdf(X, Y):
      return Y[:, 0]

    n_queries = 10**3
    X = np.ones((n_queries, 2)) * 2
    Y = np.stack([np.linspace(-3, 3, num=n_queries), np.linspace(-3, 3, num=n_queries)], axis=-1)
    p_true = pdf(X, Y)

    p_batched = execute_batch_async_pdf(pdf, X, Y, batch_size=10000)

    self.assertLessEqual(np.mean((p_true - p_batched)**2), 0.00001)

  def test_batch_exec_2(self):
    from scipy.stats import multivariate_normal

    def pdf(X, Y):
      std = 1
      ndim_y = Y.shape[1]
      return multivariate_normal.pdf(Y, mean=np.zeros(ndim_y), cov=np.eye(ndim_y)*std**2)

    n_queries = 8*10 ** 4
    X = np.ones((n_queries, 2)) * 2
    Y = np.stack([np.linspace(-3, 3, num=n_queries), np.linspace(-3, 3, num=n_queries)], axis=-1)
    p_true = pdf(X, Y)

    p_batched = execute_batch_async_pdf(pdf, X, Y, batch_size=10000, n_jobs=8)

    self.assertLessEqual(np.mean((p_true - p_batched) ** 2), 0.00001)

class TestIntegration(unittest.TestCase):

  def test_integration1(self):
    skew = lambda x: x ** 3 * stats.norm.pdf(x).flatten()

    result = numeric_integation(skew, n_samples=10**5)
    print("skew", result)
    self.assertAlmostEqual(float(result), 0.0, places=1)

    kurt = lambda x: x**4 * stats.norm.pdf(x).flatten()

    result = numeric_integation(kurt, n_samples=10**5)
    print("kurt", result)
    self.assertAlmostEqual(float(result), 3, places=1)

class TestDistribution(unittest.TestCase):

  def test_multidim_student_t(self):
    from scipy.stats import t
    from cde.utils.distribution import multidim_t_pdf
    mu = 5 * np.ones(3)
    sigma = 3 * np.ones(3)
    dof = 6

    x = np.random.uniform(-10, 10, size=(100, 3))
    p1 = np.prod(t.pdf(x, loc=5, scale=3, df=dof), axis=-1)

    p2 = multidim_t_pdf(x, mu, sigma, dof)

    self.assertLessEqual(np.sum((p1 - p2)**2), 0.0001)

  def test_batched_student_t_pdf(self):
    locs = np.random.normal(0, 3, size=10)
    scales = np.random.uniform(0.1, 10, size=10)
    dofs = np.random.uniform(3, 10, size=10)
    x = np.random.normal(0, 3, size=10)

    p = batched_univ_t_pdf(x, locs, scales, dofs)
    assert p.shape == (10,)

    for i in range(10):
      p_check = stats.t.pdf(x[i], df=dofs[i], loc=locs[i], scale=scales[i])
      self.assertAlmostEqual(p_check, p[i])

  def test_batched_student_t_cdf(self):
    locs = np.random.normal(0, 3, size=10)
    scales = np.random.uniform(0.1, 10, size=10)
    dofs = np.random.uniform(3, 10, size=10)
    x = np.random.normal(0, 3, size=10)

    p = batched_univ_t_cdf(x, locs, scales, dofs)
    assert p.shape == (10,)

    for i in range(10):
      p_check = stats.t.cdf(x[i], df=dofs[i], loc=locs[i], scale=scales[i])
      self.assertAlmostEqual(p_check, p[i])

  def test_batched_student_t_rvs(self):
    np.random.seed(123)
    n = 5000
    locs = np.ones(n) * 5
    scales = np.ones(n) * 2
    dofs = np.ones(n) * 4

    rvs = batched_univ_t_rvs(locs, scales, dofs)

    cdf_callable = lambda y: stats.t.cdf(y, df=4, loc=5, scale=2)
    _, p_val = stats.kstest(rvs, cdf_callable)
    print("P-Val Kolmogorov:", p_val)

    self.assertGreaterEqual(p_val, 0.1)

if __name__ == '__main__':
  warnings.filterwarnings("ignore")

  testmodules = [
    'unittests_utils.TestHelpers',
    'unittests_utils.TestExecAsyncBatch',
    'unittests_utils.TestIntegration',
    'unittests_utils.TestDistribution',
   ]
  suite = unittest.TestSuite()
  for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

  unittest.TextTestRunner().run(suite)
