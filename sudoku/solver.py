# get next variable
# get next value
# to dict
from variable import Variable
from backtrace import BackTrace
import queue

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


class Solver:

    def __init__(self,board):
        self.hassolution = False
        self.variables = []
        self.unchangeable = []
        self.backtrace = BackTrace()
        for i in board.keys():
            value = board[i]
            if value == 0:
                variable = Variable(i,list(range(1,10)))
                self.variables.append(variable)
            else:
                variable = Variable(i,[value])
                self.unchangeable.append(variable)
        self.basicCheck()

    def basicCheck(self):
        for var in self.variables:
            for unchange in self.unchangeable:
                if unchange.isNeibor(var):
                    var.removeValueFromDomain(unchange.getAssignment())

    def getNeighbors(self,var):
        neihobors = []
        for unchange in self.unchangeable:
            if var.isNeibor(unchange) and not var == unchange:
                neihobors.append(unchange)
        for variable in self.variables:
            if var.isNeibor(variable) and not var == variable:
                neihobors.append(variable)
        return neihobors

    def getMRV(self):
        minlen = 10
        result = None
        for var in self.variables:
            if not var.isAssigned():
                if len(var.getValues()) < minlen:
                    minlen = len(var.getValues())
                    result = var
        return result

    def getValuesLCVOrder(self,var):
        return var.getValues()

    def forwardChecking(self):
        for var in self.variables:
            if var.isAssigned() and not var.isFChecked():
                var.setFChecked(True)
                for n in self.getNeighbors(var):
                    if n.isAssigned() and n.getAssignment() == var.getAssignment():
                        var.setFChecked(False)
                        return False
                    self.backtrace.push(n)
                    n.removeValueFromDomain(var.getAssignment())
        return True

    def solve(self):
        if self.hassolution:
            return

        # Variable Selection
        v = self.getMRV()
        # check if the assigment is complete
        if v is None:
            for var in self.variables:
                # If all variables haven't been assigned
                if not var.isAssigned():
                    print("Error")
            # Success
            self.hassolution = True
            return
        # print(v.getName())
        # Attempt to assign a value
        for i in self.getValuesLCVOrder(v):

            # Store place in trail and push variable's state on trail
            self.backtrace.placeTrailMarker()
            self.backtrace.push(v)

            # Assign the value
            v.assignValue(i)

            # Propagate constraints, check consistency, recurse
            if self.forwardChecking():
                self.solve()

            # If this assignment succeeded, return
            if self.hassolution:
                return

            # Otherwise backtrack
            self.backtrace.undo()


    def to_dict(self):
        result = {}
        for var in self.unchangeable:
            result[var.getName()] = var.getAssignment()
        for var in self.variables:
            result[var.getName()] = var.getAssignment()
        sorted(result)
        return result
