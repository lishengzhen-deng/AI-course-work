class Variable:
    def __init__(self, name, values):
        self.name = name
        self.values = values
        if len(values) == 1:
            self.fchecked = True
            self.changeable = False
        else:
            self.fchecked = False
            self.changeable = True

    def copy(self, v):
        self.name = v.name
        self.values = v.values
        self.fchecked = v.fchecked
        self.changeable = v.changeable

    def isChangeable(self):
        return self.changeable

    def isAssigned(self):
        return len(self.values) == 1

    def isFChecked(self):
        return self.fchecked

    # Returns the assigned value or 0 if unassigned
    def getAssignment(self):
        if not self.isAssigned():
            return 0
        else:
            return self.values[0]

    def getName(self):
        return self.name

    def getValues(self):
        return self.values

    def setFChecked(self, mod):
        self.fchecked = mod

    def setValues(self, values):
        self.values = values
    # Assign a value to the variable
    def assignValue(self, val):
        if not self.changeable:
            return
        self.values = [val]

    # Removes a value from the domain
    def removeValueFromDomain(self, val):
        if not self.changeable:
            return
        if val not in self.getValues():
            return
        self.values.remove(val)

    def isNeibor(self, var):
        sameColumn = self.name[0] == var.getName()[0]
        sameRow = self.name[1] == var.getName()[1]

        selfblockcol = (ord(self.name[0]) - ord('A')) // 3
        selfblockrow = (ord(self.name[1]) - ord('1')) // 3
        varblockcol = (ord(var.getName()[0]) - ord('A')) // 3
        varblockrow = (ord(var.getName()[1]) - ord('1')) // 3

        sameBlock = selfblockcol == varblockcol and selfblockrow == varblockrow


        return sameRow or sameBlock or sameColumn
