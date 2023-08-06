import pytest
import numbers
import discretisedfield as df
import micromagneticmodel as mm


class TestZhangLi:
    def setup(self):
        self.valid_args = [(1, 1),
                           (-1.0, 2.0),
                           (0, 5e-11),
                           (19, -1e-12),
                           ({'r1': 1, 'r2': 2}, 0.5)]
        self.invalid_args = [((1, -2), 1),
                             (-1.0, '2.0'),
                             ((0, 0, 0, 9), 5e-11),
                             (11, -1e-12+2j),
                             (1, {'r1 2': 1, 'r2': 2})]

    def test_init_valid_args(self):
        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta)
            assert term.beta == beta
            assert isinstance(term.beta, (numbers.Real, dict))
            assert term.name == 'zhangli'

    def test_init_invalid_args(self):
        for u, beta in self.invalid_args:
            with pytest.raises(Exception):
                term = mm.ZhangLi(u=u, beta=beta)

    def test_repr_latex_(self):
        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta)
            assert isinstance(term._repr_latex_(), str)

    def test_repr(self):
        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta)
            assert isinstance(repr(term), str)

    def test_script(self):
        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta)
            with pytest.raises(NotImplementedError):
                script = term._script

    def test_field(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        field = df.Field(mesh, dim=1, value=1)
        term = mm.ZhangLi(u=field, beta=0.5)
        assert isinstance(term.u, df.Field)

    def test_kwargs(self):
        for u, beta in self.valid_args:
            term = mm.ZhangLi(u=u, beta=beta, e=1, something='a')
            assert term.e == 1
            assert term.something == 'a'
