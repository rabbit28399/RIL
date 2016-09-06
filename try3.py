d = {'zest': ['zested', 157], 'zip': ['zipped', 693, 'zipped', 4668], 'zoom': ['zoomed', 1299, 'zoomed', 7193], 'zigzag': ['zigzagged', 651, 'zigzagged', 66], 'zero': ['zeroed', 227, 'zeroed', 1235], 'zinc': ['-', 0], 'zone': ['zoned', 37969, 'zoned', 8033, 'zoned', 209], 'zipper': ['-', 0]}

sums = {k:sum(map(int, v)) for k, v in d.items()}
print sums
