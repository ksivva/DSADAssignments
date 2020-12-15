import sys


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

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, curr_node):
        if curr_node is not None:
            self._print_tree(curr_node.left)
            print(str(curr_node.empId) + " - " + str(curr_node.attCtr))
            self._print_tree(curr_node.right)

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

    def _recordSwipeRec(self, eNode, Eid):
        tree = EmpSearchTree()
        f = open("inputPS23.txt", "r")
        lines = f.readlines()
        for line in lines:
            tree.insert(line)
        f.close()

    def _getSwipeRec(self, eNode):
        tree = EmpSearchTree()
        f = open("inputPS23.txt", "r")
        lines = f.readlines()
        count = 0;
        for line in lines:
            tree.insert(line)
            count += 1
        f.close()
        sys.stdout = open("outputPS23.txt", "w")
        print("Total number of employees recorded today: " + str(count))
        sys.stdout.close()


def main():
    employeeTree = EmpSearchTree()
    count_of_employees_on_premises = 0
    count_of_employees_greater_than_freq = 0
    # employeeTree.getSwipeRec(employeeTree)
    f = open("inputPS23.txt", "r")
    lines = f.readlines()
    for line in lines:
        employeeTree.insert(line.rstrip())
    f.close()
    p = open("promptsPS23.txt", "r")
    prompts = p.readlines()
    sys.stdout = open("outputPS23.txt", "w")
    for prompt in prompts:
        if prompt.startswith('onPremises:', 0, len(prompt)):
            count_of_employees_on_premises = get_employee_count_on_premises(count_of_employees_on_premises,
                                                                            employeeTree, prompt)
        if prompt.startswith('checkEmp:', 0, len(prompt)):
            employee_id = prompt[len("checkEmp:"):].rstrip()
            employee = employeeTree.search(employee_id)
            if employee is not None:
                if employee.attCtr % 2 == 0:
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

    if count_of_employees_on_premises == 0:
        print("No employees present on premises.")
    else:
        print(str(count_of_employees_on_premises) + " employees still on premises")

    sys.stdout.close()


def get_employee_count_on_premises(count_of_employees_on_premises, employeeTree, prompt):
    employee_id = prompt[len("onPremises:"):].rstrip()
    employee = employeeTree.search(employee_id)
    if employee is not None:
        print(employee.attCtr)
        if employee.attCtr % 2 != 0:
            count_of_employees_on_premises = count_of_employees_on_premises + 1
    return count_of_employees_on_premises


if __name__ == '__main__':
    main()
