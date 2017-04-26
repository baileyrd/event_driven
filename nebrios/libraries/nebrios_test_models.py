from nebriosmodels import NebriOSModel, NebriOSField


class TestModel(NebriOSModel):

    test_a = NebriOSField()
    test_b = NebriOSField(default="abc 123")
