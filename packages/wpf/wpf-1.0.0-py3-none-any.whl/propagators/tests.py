import unittest

from propagators.sspade import *
from uwa.source import GaussSource

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

__author__ = 'Lytaev Mikhail (mikelytaev@gmail.com)'


def energy_conservation(f: HelmholtzField, eps=1e-11) -> bool:
    norms = np.linalg.norm(f.field, axis=1)
    return np.all(np.abs(norms - norms[0]) < eps)


def decaying(arr, eps) -> bool:
    return np.all(arr[1::] < arr[:-1:] + eps)


def energy_decaying(f: HelmholtzField, x_start_m=0, eps=1e-7) -> bool:
    x_i = abs(f.x_grid_m - x_start_m).argmin()
    norms = np.linalg.norm(f.field[x_i::, :], axis=1)
    return decaying(norms, eps)


def local_bc(lbc):
    env = HelmholtzEnvironment(x_max_m=1000,
                               z_min=0,
                               z_max=300,
                               lower_bc=lbc,
                               upper_bc=lbc,
                               use_n2minus1=False,
                               use_rho=False)

    src = GaussSource(freq_hz=1, depth=150, beam_width=15, eval_angle=0)
    wavelength = 1
    k0 = 2*cm.pi / wavelength
    params = HelmholtzPropagatorComputationalParams(exp_pade_order=(7, 8), max_src_angle=src.max_angle(), dz_wl=0.5, dx_wl=50)
    propagator = HelmholtzPadeSolver(env=env, wavelength=wavelength, freq_hz=300e6, params=params)
    initials_fw = [np.empty(0)] * propagator.n_x
    initials_fw[0] = np.array([src.aperture(k0, z) for z in propagator.z_computational_grid])
    f, r = propagator._propagate(initials=initials_fw, direction=1)

    # plt.imshow(10*np.log10(np.abs(f.field.T[::-1, :])), cmap=plt.get_cmap('jet'), norm=Normalize(-50, 10))
    # plt.colorbar(fraction=0.046, pad=0.04)
    # plt.show()
    return f


def transparent_const_bc(src):
    env = HelmholtzEnvironment(x_max_m=5000,
                               z_min=0,
                               z_max=300,
                               lower_bc=TransparentBC(),
                               upper_bc=TransparentBC(),
                               use_n2minus1=False,
                               use_rho=False)

    wavelength = 0.1
    k0 = 2 * cm.pi / wavelength
    params = HelmholtzPropagatorComputationalParams(exp_pade_order=(7, 8), max_src_angle=src.max_angle(), dz_wl=0.5,
                                                    dx_wl=50, tol=1e-11)
    propagator = HelmholtzPadeSolver(env=env, wavelength=wavelength, freq_hz=300e6, params=params)
    initials_fw = [np.empty(0)] * propagator.n_x
    initials_fw[0] = np.array([src.aperture(k0, z) for z in propagator.z_computational_grid])
    f, r = propagator._propagate(initials=initials_fw, direction=1)

    # plt.imshow(10 * np.log10(np.abs(f.field.T[::-1, :])), cmap=plt.get_cmap('jet'), norm=Normalize(-50, 10))
    # plt.colorbar(fraction=0.046, pad=0.04)
    # plt.show()
    return f


def transparent_const_bc_cn(src):
    env = HelmholtzEnvironment(x_max_m=5000,
                               z_min=0,
                               z_max=300,
                               lower_bc=TransparentBC(),
                               upper_bc=TransparentBC(),
                               use_n2minus1=False,
                               use_rho=False)

    wavelength = 0.1
    k0 = 2 * cm.pi / wavelength
    params = HelmholtzPropagatorComputationalParams(exp_pade_order=(1, 1), max_src_angle=src.max_angle())
    propagator = HelmholtzPadeSolver(env=env, wavelength=wavelength, freq_hz=300e6, params=params)
    initials_fw = [np.empty(0)] * propagator.n_x
    initials_fw[0] = np.array([src.aperture(k0, z) for z in propagator.z_computational_grid])
    f, r = propagator._propagate(initials=initials_fw, direction=1)

    # plt.imshow(10 * np.log10(np.abs(f.field.T[::-1, :])), cmap=plt.get_cmap('jet'), norm=Normalize(-50, 10))
    # plt.colorbar(fraction=0.046, pad=0.04)
    # plt.show()
    return f


class HelmholtzPropagatorTest(unittest.TestCase):

    def test_Dirichlet(self):
        #logging.basicConfig(level=logging.DEBUG)
        f = local_bc(RobinBC(1, 0, 0))
        self.assertTrue(energy_conservation(f, eps=1e-11))

    def test_Neumann(self):
        #logging.basicConfig(level=logging.DEBUG)
        f = local_bc(RobinBC(0, 1, 0))
        self.assertTrue(energy_conservation(f, eps=1e-2))

    def test_transparent_const(self):
        #logging.basicConfig(level=logging.DEBUG)
        src = GaussSource(freq_hz=1, depth=150, beam_width=15, eval_angle=0)
        f = transparent_const_bc(src)
        self.assertTrue(energy_decaying(f, x_start_m=20))

    def test_transparent_const_lower(self):
        #logging.basicConfig(level=logging.DEBUG)
        src = GaussSource(freq_hz=1, depth=150, beam_width=2, eval_angle=10)
        f = transparent_const_bc(src)
        self.assertTrue(energy_decaying(f, x_start_m=20))
        self.assertTrue(np.linalg.norm(f.field[-1, :]) < 5e-11)

    def test_transparent_const_upper(self):
        #logging.basicConfig(level=logging.DEBUG)
        src = GaussSource(freq_hz=1, depth=150, beam_width=2, eval_angle=-10)
        f = transparent_const_bc(src)
        self.assertTrue(energy_decaying(f, x_start_m=20))
        self.assertTrue(np.linalg.norm(f.field[-1, :]) < 5e-11)

    def test_transparent_const_lower_cn(self):
        #logging.basicConfig(level=logging.DEBUG)
        src = GaussSource(freq_hz=1, depth=150, beam_width=2, eval_angle=10)
        f = transparent_const_bc_cn(src)
        self.assertTrue(energy_decaying(f, x_start_m=20))
        self.assertTrue(np.linalg.norm(f.field[-1, :]) < 1e-5)

    def test_transparent_const_upper_cn(self):
        #logging.basicConfig(level=logging.DEBUG)
        src = GaussSource(freq_hz=1, depth=150, beam_width=2, eval_angle=-10)
        f = transparent_const_bc_cn(src)
        self.assertTrue(energy_decaying(f, x_start_m=20))
        self.assertTrue(np.linalg.norm(f.field[-1, :]) < 1e-5)

    def test_nlbc_storage(self):
        #logging.basicConfig(level=logging.DEBUG)
        nlbc_file_name = 'nlbc'
        import os
        if os.path.isfile(nlbc_file_name):
            os.remove(nlbc_file_name)
        env = HelmholtzEnvironment(x_max_m=5000,
                                   z_min=0,
                                   z_max=300,
                                   lower_bc=TransparentBC(),
                                   upper_bc=TransparentBC(),
                                   use_n2minus1=False,
                                   use_rho=False)

        wavelength = 0.1
        src = GaussSource(freq_hz=1, depth=150, beam_width=15, eval_angle=0)
        k0 = 2 * cm.pi / wavelength
        params = HelmholtzPropagatorComputationalParams(exp_pade_order=(7, 8), max_src_angle=src.max_angle(), dz_wl=0.5,
                                                        dx_wl=50, tol=1e-11, storage=PickleStorage(nlbc_file_name))
        propagator = HelmholtzPadeSolver(env=env, wavelength=wavelength, freq_hz=300e6, params=params)
        initials_fw = [np.empty(0)] * propagator.n_x
        initials_fw[0] = np.array([src.aperture(k0, z) for z in propagator.z_computational_grid])
        f1, r = propagator._propagate(initials=initials_fw, direction=1)
        f2, r = propagator._propagate(initials=initials_fw, direction=1)

        self.assertTrue(os.path.isfile(nlbc_file_name))
        self.assertTrue(np.linalg.norm(f1.field - f2.field) < 1e-11)

    def test_tomas_method(self):
        n = 10
        b = np.random.rand(n) + 1j*np.random.rand(n)
        a = np.random.rand(n-1) + 1j*np.random.rand(n-1)
        c = np.random.rand(n-1) + 1j*np.random.rand(n-1)
        matrix = np.diag(b, 0) + np.diag(a, -1) + np.diag(c, 1)
        rhs = np.random.rand(n) + 1j*np.random.rand(n)
        res1 = np.linalg.solve(matrix, rhs)
        res2 = tridiag_method(a, b, c, rhs)
        self.assertTrue(np.linalg.norm(res1 - res2)/np.linalg.norm(res1) < 1e-5)

    def test_lentz(self):
        tol = 1e-14
        self.assertTrue(abs(lentz(lambda n: (n > 1) * 2.0 + (n < 2) * 1.0, tol) - fm.sqrt(2)) < tol)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    HelmholtzPropagatorTest.main()
