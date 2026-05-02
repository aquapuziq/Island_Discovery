from collections import defaultdict

def dfs(graph, start_v):
    visited = set()
    st = [start_v]

    while st:
        node = st.pop()
        if node in visited:
            continue

        visited.add(node)
        for i in range(len(graph[node]) - 1, -1, -1):
            v = graph[node][i][0]
            if v not in visited:
                st.append(v)
    return visited

def find_components(graph):
    visited = set()
    components = []

    for start_v in graph:
        if start_v not in visited:
            component = dfs(graph, start_v)
            components.append(component)
            for v in component:
                visited.add(v)
    return components

def is_island(graph):
    for v in graph:
        deg = len(graph[v])
        if deg % 2 == 1:
            return False
    return True

def hierholzer(graph, start_v):
    stack = [(start_v, None)]
    path = []
    tmp_graph = {u: list(edges) for u, edges in graph.items()}

    while stack:
        v, points_tmp = stack[-1]
        if tmp_graph[v]:
            u, points = tmp_graph[v].pop()
            for i, (n, c) in enumerate(tmp_graph[u]):
                if n == v and c == list(points[::-1]):
                    tmp_graph[u].pop(i)
                    break
            stack.append((u, points))
        else:
            path.append(stack.pop())

    path.reverse()
    circuit = []
    for v, points in path:
        if points is None:
            continue
        if not circuit:
            circuit.extend(points)
        else:
            if points[0] != circuit[-1]:
                points = points[::-1]
            circuit.extend(points[1:])
    return circuit

def build_graph(segments):
    gr = defaultdict(list)
    for segment in segments:
        start_v = tuple(segment[0])
        end_v = tuple(segment[-1])
        path = [tuple(p) for p in segment]

        gr[start_v].append((end_v, path))
        gr[end_v].append((start_v, path[::-1]))
    return gr

def group_by_type(features):
    groups = defaultdict(list)
    for feat in features:
        if feat["geometry"]["type"] == "LineString":
            type_obj = feat["properties"]["type"]
            groups[type_obj].append(feat["geometry"]["coordinates"])
    return groups

def find_islands(segments):
    islands = []
    graph = build_graph(segments)
    components = find_components(graph)
    for component in components:
        tmp = {v: graph[v] for v in component}
        if is_island(tmp):
            islands.append(hierholzer(tmp, next(iter(tmp))))
        else:
            continue
    return islands

def islands_groups(groups):
    islands_gr = defaultdict(list)
    for key, val in groups.items():
        islands = find_islands(val)
        islands_gr[key].extend(islands)
    return islands_gr
