import os
import shutil
import pytest
import oommfc as oc
import discretisedfield as df


def test_skyrmion():
    name = 'skyrmion'

    # Remove any previous simulation directories.
    if os.path.exists(name):
        shutil.rmtree(name)

    Ms = 1.1e6
    A = 1.6e-11
    D = 4e-3
    K = 0.51e6
    u = (0, 0, 1)
    H = (0, 0, 2e5)

    mesh = oc.Mesh(p1=(-50e-9, -50e-9, 0),
                   p2=(50e-9, 50e-9, 10e-9),
                   cell=(5e-9, 5e-9, 5e-9))

    system = oc.System(name=name)
    system.hamiltonian = oc.Exchange(A=A) + \
        oc.DMI(D=D, crystalclass='Cnv') + \
        oc.UniaxialAnisotropy(K1=K, u=u) + \
        oc.Demag() + \
        oc.Zeeman(H=H)

    def Ms_fun(pos):
        x, y, z = pos
        if (x**2 + y**2)**0.5 < 50e-9:
            return Ms
        else:
            return 0

    def m_init(pos):
        x, y, z = pos
        if (x**2 + y**2)**0.5 < 10e-9:
            return (0, 0.1, -1)
        else:
            return (0, 0.1, 1)

    system.m = df.Field(mesh, value=m_init, norm=Ms_fun)

    md = oc.MinDriver()
    md.drive(system)

    # Check the magnetisation at the sample centre.
    value = system.m((0, 0, 0))
    print(value)
    assert value[2]/Ms < -0.97

    # Check the magnetisation at the sample edge.
    value = system.m((50e-9, 0, 0))
    assert value[2]/Ms > 0.5

    system.delete()
