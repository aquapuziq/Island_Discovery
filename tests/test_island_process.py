from head.island_process import build_graph, is_island, find_islands, group_by_type, islands_groups
import json

def test_build_graph():
    segments = [[[0,0], [0,1]]]
    graph = build_graph(segments)
    assert graph == {(0, 0): [((0, 1), [(0, 0), (0, 1)])], (0, 1): [((0, 0), [(0, 1), (0, 0)])]}

def test_is_island():
    segments = [
        [[0, 0], [0, 1]],
        [[0, 1], [1, 1]],
        [[1, 1], [0, 0]],
    ]
    graph = build_graph(segments)
    assert is_island(graph) == True

def test_find_islands():
    segments = [
        [[0,0], [0,1]],
        [[0,1], [1,1], [1,0], [0,0]]
    ]
    check_tmp = find_islands(segments)
    assert len(check_tmp) == 1
    assert check_tmp[0] == [(0, 1), (1, 1), (1, 0), (0, 0), (0, 1)]

def test_group_by_type_from_json():
    with open("test_islands.json") as file:
        data = json.load(file)
    groups = group_by_type(data["features"])
    assert groups == {'a': [[[0, 0], [0, 1]], [[0, 1], [1, 1], [1, 0], [0, 0]]], 'noise': [[[5, 5], [6, 6]]]}

def test_find_islands_no_circuit():
    segments = [
        [[0,0], [1,1]],
        [[1,1], [2,2]],
    ]
    res = find_islands(segments)
    assert res == []

def test_find_islands_many():
    segments = [
        [[0, 0], [0, 1]],
        [[0, 1], [1, 1]],
        [[1, 1], [0, 0]],

        [[5, 5], [5, 6]],
        [[5, 6], [6, 6]],
        [[6, 6], [5, 5]],

        [[10, 10], [10, 11]],
        [[10, 11], [11, 11]],
        [[11, 11], [10, 10]],
    ]
    check_tmp = find_islands(segments)
    assert len(check_tmp) == 3
    assert check_tmp[0] == [(0, 1), (1, 1), (0, 0), (0, 1)]
    assert check_tmp[1] == [(6, 6), (5, 5), (5, 6), (6, 6)]
    assert check_tmp[2] == [(10, 10), (11, 11), (10, 11), (10, 10)]

def test_islands_groups_mixed():
    groups = {
        "a": [[[0,0],[0,1]], [[0,1],[1,1],[1,0],[0,0]]],
        "noise": [[[5,5],[6,6]]]
    }
    res = islands_groups(groups)
    assert "a" in res
    assert len(res["a"]) == 1
    assert res["noise"] == []
    assert res["a"] == [[(0, 1), (1, 1), (1, 0), (0, 0), (0, 1)]]