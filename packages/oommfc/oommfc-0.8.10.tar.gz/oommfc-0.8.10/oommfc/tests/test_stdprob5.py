import os
import glob
import shutil
import pytest
import numpy as np
import oommfc as oc
import discretisedfield as df
from scipy.optimize import bisect


@pytest.mark.oommf
def test_stdprob5():
    name = 'stdprob5'

    # Remove any previous simulation directories.
    if os.path.exists(name):
        shutil.rmtree(name)

    # Geometry
    lx = 100e-9  # x dimension of the sample(m)
    ly = 100e-9  # y dimension of the sample (m)
    lz = 10e-9  # sample thickness (m)

    # Material (permalloy) parameters
    Ms = 8e5  # saturation magnetisation (A/m)
    A = 1.3e-11  # exchange energy constant (J/m)

    # Dynamics (LLG + ZhangLi equation) parameters
    gamma = 2.211e5  # gyromagnetic ratio (m/As)
    alpha = 0.1  # Gilbert damping
    ux = -72.35  # velocity in x direction
    beta = 0.05  # non-adiabatic STT parameter

    system = oc.System(name=name)
    mesh = oc.Mesh(p1=(0, 0, 0), p2=(lx, ly, lz),
                   cell=(5e-9, 5e-9, 5e-9))
    system.hamiltonian = oc.Exchange(A) + oc.Demag()

    def m_vortex(pos):
        x, y, z = pos[0]/1e-9-50, pos[1]/1e-9-50, pos[2]/1e-9
        return (-y, x, 10)

    system.m = df.Field(mesh, value=m_vortex, norm=Ms)

    md = oc.MinDriver()
    md.drive(system)

    system.dynamics += oc.Precession(gamma) + oc.Damping(alpha) + \
        oc.ZhangLi(u=ux, beta=beta)

    td = oc.TimeDriver()
    td.drive(system, t=8e-9, n=100)

    mx = system.dt['mx'].values

    assert -0.35 < mx.min() < -0.30
    assert -0.03 < mx.max() < 0
    

    system.delete()
