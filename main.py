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
    employeeTree.getSwipeRec(employeeTree)


if __name__ == '__main__':
    main()
