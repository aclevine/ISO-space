def partition(items, k):
    """Returns k unique partitions of a sequence of items.
    
    The partitions are pairs of pair-wise disjoint parts of the items with one 
    part containing 1/k of the items and the other part containing the rest of 
    the items. Each of the k parts that contain 1/k of the items are also 
    k-wise disjoint from each other and mutually exhaustive of items.
    
    E.g.:
    
    partition('xyz', 2) -> [('x', 'yz'), ('yz', 'x')]
    
    partition(range(10), 10) -> [([0], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                 ([1], [0, 2, 3, 4, 5, 6, 7, 8, 9]),
                                 ([2], [0, 1, 3, 4, 5, 6, 7, 8, 9]),
                                 ([3], [0, 1, 2, 4, 5, 6, 7, 8, 9]),
                                 ([4], [0, 1, 2, 3, 5, 6, 7, 8, 9]),
                                 ([5], [0, 1, 2, 3, 4, 6, 7, 8, 9]),
                                 ([6], [0, 1, 2, 3, 4, 5, 7, 8, 9]),
                                 ([7], [0, 1, 2, 3, 4, 5, 6, 8, 9]),
                                 ([8], [0, 1, 2, 3, 4, 5, 6, 7, 9]),
                                 ([9], [0, 1, 2, 3, 4, 5, 6, 7, 8])]"""
    partitions = []
    length = len(items)
    if 1 < k <= length:
        for i in range(k):
            start = int(length * i / k)
            end = int(min(length * (i + 1) / k, length))
            partitions.append((items[start:end], items[:start] + items[end:]))
    return partitions
