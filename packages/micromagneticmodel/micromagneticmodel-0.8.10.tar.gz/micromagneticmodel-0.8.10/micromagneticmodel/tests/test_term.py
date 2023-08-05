import pytest
import micromagneticmodel as mm


class TestTerm:
    def test_abstract_class(self):
        with pytest.raises(TypeError):
            term = mm.util.Term()
