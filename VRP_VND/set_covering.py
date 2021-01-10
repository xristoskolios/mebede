class Subset:
    def __init__(self, id, lst):
        self.id = id
        self.coveredItems = set(lst)

def buildInput(subsets):
    s = Subset(1, [1, 2])
    subsets.append(s)
    s = Subset(2, [1, 2, 3])
    subsets.append(s)
    s = Subset(3, [3, 4, 5, 6])
    subsets.append(s)
    s = Subset(4, [2, 3, 4, 9])
    subsets.append(s)
    s = Subset(5, [4, 5, 6, 8])
    subsets.append(s)
    s = Subset(6, [6, 7])
    subsets.append(s)
    s = Subset(7, [7, 8])
    subsets.append(s)
    s = Subset(8, [5, 7, 8, 10])
    subsets.append(s)
    s = Subset(9, [4, 8, 9, 10])
    subsets.append(s)
    s = Subset(10, [8, 10])
    subsets.append(s)

universe = [i+1 for i in range(0, 10)]
subsets = []
buildInput(subsets)


selectedSubsets = []
uncoveredUniverseElementSet = set(universe)
remainingSubsetSet = set(subsets)

def IdentifyMaximizingCoverage(remainingSubsetSet, uncoveredUniverseElementSet):
    coveredElements = -1
    selected = None
    for subset in remainingSubsetSet:
        coverage = len(uncoveredUniverseElementSet.intersection(subset.coveredItems))
        if coverage > coveredElements:
            coveredElements = coverage
            selected = subset
    return selected



def RemoveCoveredUniverseElements(selected:Subset, uncoveredUniverseElementSet):
    for elem in selected.coveredItems:
        uncoveredUniverseElementSet.discard(elem)
        # error if remove is applied to an element not present in the set
        #uncoveredUniverseElementSet.remove(elem)

while len(uncoveredUniverseElementSet) > 0:
    selected = IdentifyMaximizingCoverage(remainingSubsetSet, uncoveredUniverseElementSet)
    selectedSubsets.append(selected)
    RemoveCoveredUniverseElements(selected, uncoveredUniverseElementSet)
    remainingSubsetSet.discard(selected)

print('Selected subsets:')
for sub in selectedSubsets:
    print(sub.id)
print('Objective function = ', len(selectedSubsets))
a = 0
