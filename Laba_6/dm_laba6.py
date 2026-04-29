import itertools

g1 = [(0, 1), (0, 6), (1, 2), (1, 5), (1, 6), (1, 7), (1, 8), (2, 3), (2, 5), (2, 8), (2, 9), (3, 4), (3, 6), (3, 9),
      (4, 5), (4, 7), (4, 9), (5, 6), (5, 7), (6, 7), (6, 9), (7, 8), (7, 9), (8, 9)]
g2 = [(0, 1), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 2), (1, 4), (1, 5), (1, 8), (1, 9), (2, 4), (2, 6), (2, 7),
      (2, 9), (3, 6), (3, 8), (4, 6), (5, 7), (5, 9), (6, 7), (6, 8), (7, 8), (8, 9)]

g1 = set(g1)
g2 = set(g2)

vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def is_isomorphism(mapping):
    mapped_edges = set()
    for u, v in g1:
        mu = mapping[u]
        mv = mapping[v]
        mapped_edges.add(tuple(sorted((mu, mv))))
    return mapped_edges == g2

for perm in itertools.permutations(vertices):
    mapping = {i: perm[i] for i in vertices}
    if is_isomorphism(mapping):
        print(mapping)