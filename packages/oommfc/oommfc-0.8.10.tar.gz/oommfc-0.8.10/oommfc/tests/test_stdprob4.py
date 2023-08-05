import os
import glob
import shutil
import pytest
import oommfc as oc
import discretisedfield as df
import pytest


def test_stdprob4():
    name = 'stdprob4'

    # Remove any previous simulation directories.
    if os.path.exists(name):
        shutil.rmtree(name)

    L, d, th = 500e-9, 125e-9, 3e-9   # (m)
    cell = (5e-9, 5e-9, 3e-9)  # (m)
    mesh = oc.Mesh(p1=(0, 0, 0), p2=(L, d, th), cell=cell)

    system = oc.System(name=name)

    A = 1.3e-11  # (J/m)
    system.hamiltonian = oc.Exchange(A) + oc.Demag()

    gamma = 2.211e5  # (m/As)
    alpha = 0.02
    system.dynamics = oc.Precession(gamma) + oc.Damping(alpha)

    Ms = 8e5  # (A/m)
    system.m = df.Field(mesh, value=(1, 0.25, 0.1), norm=Ms)

    md = oc.MinDriver()
    md.drive(system)  # updates system.m in-place

    dirname = os.path.join(name, 'drive-{}'.format(system.drive_number-1))
    miffilename = os.path.join(dirname, '{}.mif'.format(name))
    assert os.path.exists(dirname)
    assert os.path.isfile(miffilename)

    omf_files = list(glob.iglob('{}/*.omf'.format(dirname)))
    odt_files = list(glob.iglob('{}/*.odt'.format(dirname)))

    assert len(omf_files) == 2
    omffilename = os.path.join(dirname, 'm0.omf')
    assert omffilename in omf_files

    assert len(odt_files) == 1

    shutil.rmtree(name)

    H = (-24.6e-3/oc.consts.mu0, 4.3e-3/oc.consts.mu0, 0)
    system.hamiltonian += oc.Zeeman(H)

    td = oc.TimeDriver()
    td.drive(system, t=1e-9, n=200)

    dirname = os.path.join(name, 'drive-{}'.format(system.drive_number-1))
    miffilename = os.path.join(dirname, '{}.mif'.format(name))
    assert os.path.exists(dirname)
    assert os.path.isfile(miffilename)

    omf_files = list(glob.iglob('{}/*.omf'.format(dirname)))
    odt_files = list(glob.iglob('{}/*.odt'.format(dirname)))

    assert len(omf_files) == 201
    omffilename = os.path.join(dirname, 'm0.omf')
    assert omffilename in omf_files

    assert len(odt_files) == 1

    t = system.dt['t'].values
    my = system.dt['my'].values

    assert abs(min(t) - 5e-12) < 1e-20
    assert abs(max(t) - 1e-9) < 1e-20

    # Eye-norm test.
    assert 0.7 < max(my) < 0.8
    assert -0.5 < min(my) < -0.4

    shutil.rmtree(name)
