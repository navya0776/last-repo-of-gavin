from utils.sample import Sample

def test_testme_returns_input_for_strings():
    s = Sample()
    assert s.testme("hello") == "hello"   # expected normal behavior

def test_testme_returns_none_for_non_strings():
    s = Sample()
    assert s.testme(123) is None           # explicit handling of invalid input
    assert s.testme(['a']) is None
    assert s.testme(None) is None
