import sys

ON_PREMISES = 'onPremises:'

WRITE_MODE = "w"

READ_MODE = "r"

OUTPUT_FILE_NAME = "outputPS23.txt"

PROMPTS_FILE_NAME = "promptsPS23.txt"

INPUT_FILE_NAME = "inputPS23.txt"

RANGE = "range:"

FREQ_VISIT = "freqVisit:"

CHECK_EMP = 'checkEmp:'


class EmpNode:
    def __init__(self, EId):
        self.empId = EId
        self.attCtr = 1
        self.left = None
        self.right = None


class EmpSearchTree:
    def __init__(self):
        self.root = None

    def insert(self, EId):
        if self.root is None:
            self.root = EmpNode(EId)
        else:
            self._insert(EId, self.root)

    def _insert(self, EId, curr_node):
        if EId == curr_node.empId:
            curr_node.attCtr = curr_node.attCtr + 1
            return curr_node
        if EId < curr_node.empId:
            if curr_node.left is None:
                curr_node.left = EmpNode(EId)
            else:
                self._insert(EId, curr_node.left)
        else:
            if curr_node.right is None:
                curr_node.right = EmpNode(EId)
            else:
                self._insert(EId, curr_node.right)
        if EId == curr_node.empId:
            curr_node.attCtr = curr_node.attCtr + 1

    def frequentVisitorRec(self, freq_visit):
        if self.root is not None:
            self._frequentVisitorRec(self.root, freq_visit)

    def _frequentVisitorRec(self, curr_node, freq_visit):
        if curr_node is not None:
            self._frequentVisitorRec(curr_node.left, freq_visit)
            if curr_node.attCtr > int(freq_visit):
                print(str(curr_node.empId) + " , " + str(curr_node.attCtr))
            self._frequentVisitorRec(curr_node.right, freq_visit)

    def onPremisesRec(self, count_of_employees_on_premises):
        if self.root is not None:
            count_of_employees_on_premises = self._onPremisesRec(self.root, count_of_employees_on_premises)
        return count_of_employees_on_premises

    def _onPremisesRec(self, curr_node, count_of_employees_on_premises):
        if curr_node is not None:
            self._onPremisesRec(curr_node.left, count_of_employees_on_premises)
            if curr_node.attCtr % 2 != 0:
                count_of_employees_on_premises = count_of_employees_on_premises + 1
            count_of_employees_on_premises = self._onPremisesRec(curr_node.right, count_of_employees_on_premises)
        return count_of_employees_on_premises

    def search(self, value):
        if self.root is not None:
            return self._search(value, self.root)
        else:
            return None

    def _search(self, value, curr_node):
        if value == curr_node.empId:
            return curr_node
        elif value < curr_node.empId and curr_node.left is not None:
            return self._search(value, curr_node.left)
        elif value > curr_node.empId and curr_node.right is not None:
            return self._search(value, curr_node.right)
        else:
            return None

    def _recordSwipeRec(self):
        tree = EmpSearchTree()
        f = open(INPUT_FILE_NAME, READ_MODE)
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if line.isnumeric():
                tree.insert(line)
            else:
                print(str(line) + " is not a number. Please enter a numeric value")
        f.close()

    def getSwipeRec(self):
        tree = EmpSearchTree()
        f = open(INPUT_FILE_NAME, READ_MODE)
        lines = f.readlines()
        count = 0
        lines = set(lines)
        for line in lines:
            line = line.rstrip()
            if line.isnumeric():
                tree.insert(line)
                count += 1
            else:
                print(str(line) + " is not a number. Please enter a numeric value")
        return count


def main():
    employee_tree = EmpSearchTree()
    count_of_employees_on_premises = 0
    sys.stdout = open(OUTPUT_FILE_NAME, WRITE_MODE)

    emploee_count = employee_tree.getSwipeRec()
    print("Total number of employees recorded today: " + str(emploee_count))
    f = open(INPUT_FILE_NAME, READ_MODE)
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        if line.isnumeric():
            employee_tree.insert(line)
        else:
            print(str(line) + " is not a number. Please enter a numeric value")
    p = open(PROMPTS_FILE_NAME, READ_MODE)
    prompts = p.readlines()
    for prompt in prompts:
        if prompt.startswith(ON_PREMISES, 0, len(prompt)):
            count_of_employees_on_premises = employee_tree.onPremisesRec(count_of_employees_on_premises)
            if count_of_employees_on_premises == 0:
                print("No employees present on premises.")
            else:
                print(str(count_of_employees_on_premises) + " employees still on premises")
        if prompt.startswith(CHECK_EMP, 0, len(prompt)):
            checkEmpRec(employee_tree, prompt)
        if prompt.startswith(FREQ_VISIT, 0, len(prompt)):
            freq_visit = prompt[len(FREQ_VISIT):].rstrip()
            print("Employees that swiped more than " + str(freq_visit) + " number of times today are: ")
            employee_tree.frequentVisitorRec(freq_visit)
        if prompt.startswith(RANGE, 0, len(prompt)):
            printRangePresent(employee_tree, lines, prompt)

    sys.stdout.close()
    f.close()


def printRangePresent(employee_tree, lines, prompt):
    min_value = prompt[len(RANGE):].rstrip().split(":")[0]
    max_value = prompt[len(RANGE):].rstrip().split(":")[1]
    print("Range: " + str(min_value) + " to " + str(max_value))
    print("Employee swipe : ")
    lines = set(lines)
    for employee_id in lines:
        employee_id = employee_id.rstrip()
        if employee_id.isnumeric() and min_value.isnumeric() and max_value.isnumeric():
            if int(min_value) <= int(employee_id) <= int(max_value):
                employee = employee_tree.search(employee_id)
                print(str(employee_id) + " , " + str(employee.attCtr) + " , " + isEmployeeInOrOut(employee.attCtr))
        else:
            print(str(employee_id) + " or " + str(min_value) + " or " + str(
                max_value) + " is not a number. Please enter a numeric value")


def checkEmpRec(employee_tree, prompt):
    employee_id = prompt[len(CHECK_EMP):].rstrip()
    if employee_id.isnumeric():
        employee = employee_tree.search(employee_id)
        if employee is not None:
            if isNumberEven(employee.attCtr):
                print(
                    "Employee id " + str(employee.empId) + " swiped " + str(
                        employee.attCtr) + " times today and is "
                                           "currently outside "
                                           "office")
            else:
                print(
                    "Employee id " + str(employee.empId) + " swiped " + str(
                        employee.attCtr) + " times today and is "
                                           "currently in "
                                           "office")
        else:
            print("Employee id " + str(employee_id) + " did not swipe today")
    else:
        print(str(employee_id) + " is not a number. Please enter a numeric value")


def isNumberEven(number):
    if number % 2 == 0:
        result = True
    else:
        result = False
    return result


def isEmployeeInOrOut(swipeCount):
    if isNumberEven(swipeCount):
        result = "out"
    else:
        result = "in"
    return result


if __name__ == '__main__':
    main()
