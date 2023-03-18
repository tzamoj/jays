from jays import j

from .utils import QueryTestCase


cases = {
    "select_slice_1": QueryTestCase(
        query=j[0:4:1],
        data=[0, 1, 2, 3],
        expected=[0, 1, 2, 3],
    ),
    "select_slice_2": QueryTestCase(
        query=j[0:4],
        data=[0, 1, 2, 3],
        expected=[0, 1, 2, 3],
    ),
    "select_slice_3": QueryTestCase(
        query=j[0:3],
        data=[0, 1, 2, 3],
        expected=[0, 1, 2],
    ),
    "select_slice_4": QueryTestCase(
        query=j[:2],
        data=[0, 1, 2, 3],
        expected=[0, 1],
    ),
    "select_slice_5": QueryTestCase(
        query=j[::2],
        data=[0, 1, 2, 3],
        expected=[0, 2],
    ),
    "select_slice_6": QueryTestCase(
        query=j[::-1],
        data=[0, 1, 2, 3],
        expected=[3, 2, 1, 0],
    ),
    "select_slice_7": QueryTestCase(
        query=j[-2:],
        data=[0, 1, 2, 3],
        expected=[2, 3],
    ),
    "select_seq_slice": QueryTestCase(
        query=j[0, :2],
        data=[[1, 2, 3, 4], [5, 6, 7]],
        expected=[1, 2],
    ),
    "select_slices": QueryTestCase(
        query=j[:, :2],
        data=[[1, 2, 3, 4], [5, 6, 7], [8]],
        expected=[[1, 2], [5, 6], [8]],
    ),
    "select_slices_piped": QueryTestCase(
        query=j[:][:2],
        data=[[1, 2, 3, 4], [5, 6, 7], [8]],
        expected=[[1, 2, 3, 4], [5, 6, 7]],
    ),
    "no_pipe": QueryTestCase(
        query=j["foo", :, "bar", 0],
        data= {"foo": [{"bar": ["first1", "second1"]}, {"bar": ["first2", "second2"]}]},
        expected=["first1", "first2"],
    ),
    "pipe": QueryTestCase(
        query=j["foo", :, "bar"][0],
        data= {"foo": [{"bar": ["first1", "second1"]}, {"bar": ["first2", "second2"]}]},
        expected=["first1", "second1"],
    ),
}
