from variable import Variable


class BackTrace:

    def __init__(self):
        self.trailStack = []
        self.trailMarker = []

    # Places a marker in the trail
    def placeTrailMarker(self):
        self.trailMarker.append(len(self.trailStack))

    # Before assign a variable, save its initial domain on the backtrace.
    # When the path fails, it can restore propagated domains correctly.
    def push(self, v):
        vPair = (v, [i for i in v.getValues()])
        self.trailStack.append(vPair)

    # Pops and restores variables on the trail until the last trail marker
    def undo(self):
        targetSize = self.trailMarker.pop()  # targetSize target position on the trail to backtrack to
        size = len(self.trailStack)
        while size > targetSize:
            vPair = self.trailStack.pop()
            v = vPair[0]
            v.setValues(vPair[1])
            v.setFChecked(False)
            size -= 1

    # Clears the trail
    def clear(self):
        self.trailStack = []
        self.trailMarker = []
