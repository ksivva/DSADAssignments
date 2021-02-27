import sys
import os.path as path

"""
 This class is a untility to select the optimum number of missions for ISRO with in specified budget
 This problem can be solved using 0/1 Knapsack problem since we want to maximize values with in budget constraits
 To initialize class you need input file name consists of <Mission name i> / < Budget bi(crores)> / < Value vi>
 and allowed budget in integer as second value
"""
class ISROMissionApprover:
    # Default constructor
    def __init__(self,file_name, allocated_budget):
        # Allocated Budget capacity in crores 
        self.allocated_budget = allocated_budget
        # Initializing missions
        self.missions = []
        # Initializing budgets array
        self.budgets = []
        # Initializing values array
        self.values = []
        # Initializing number of missions/budgets
        self.no_of_missions = 0
        
        # To read input file from the same location "inputPS8.txt"
        self.read_input(file_name)        
        
       
        
        # Initializing output variables needed
        # Initializing selected_missions to empty list
        self.selected_missions = []
        # Initializing total profit for selected missions with 0
        self.total_value = 0
        # Initializing remaining budget after selected missions with allocated_budget
        self.remaining_budget = self.allocated_budget
        
        # Initialize the missionValue matrix
        self.mission_value_matrix = [[-1 for i in range(allocated_budget + 1)] for j in range(self.no_of_missions + 1)]
        
    """
        This functions reads the input text file having filepath given as argument in read-only mode and fills the variables of class
        this is inturn called by constructor to make next operation ready
    """
    def read_input(self, file_name):
        if not path.exists(file_name):
            print('Input file does not exists')
            return
        input_file = None
        try:
            # Opening input text file
            input_file = open(file_name,'rt')
            # Reading all lines in the text
            lines = input_file.readlines()
            for line in lines:
                # Split the input by character '/'
                details = line.strip().split('/')
                mission_name = details[0].strip()
                budget = details[1].strip()
                value = details[2].strip()                                   
                    
                if not budget.isnumeric()  or (budget.isnumeric() and int(budget) < 0):
                    print('Invalid budget', budget)
                    continue
                    
                if not value.isnumeric() or (value.isnumeric() and int(value) < 0):
                    print('Invalid profit', value)
                    continue
                # Reading mission number/name
                self.missions.append(mission_name) # mission number/name
                # Reading mission's budget
                self.budgets.append(int(budget)) # weight
                # Reading mission's profit
                self.values.append(int(value)) # profit
        except Exception as ex:
            print('Error in reading input file to disk ',sys.exc_info())
            raise Exception('Invalid input given input file')
        finally:
            if input_file != None:
                input_file.close()
       
        self.no_of_missions = len(self.missions)
    
    """
       This is the actual function which calculates maximum profit can be achieved with the given budget and values with a budget constraints
       this is recursive in nature with the time complexity O(n*totalBudget_allowed )
    """
    def find_maximum_profit(self,budgets, values, allocated_budget, no_of_missions):
        if allocated_budget < 0:
            print('Invalid budget')
            return 
        if no_of_missions < 0:
            print('Invalid number of missions')
            return 
        # base conditions
        if no_of_missions == 0 or allocated_budget == 0:
            return 0
        # To reduce the steps which are repeating, we are picking up the values straitaway without repeating the entire path in recursion tree
        if  self.mission_value_matrix[no_of_missions][allocated_budget] != -1:
            
            return self.mission_value_matrix[no_of_missions][allocated_budget]
        
        # choice diagram code
        previous_mission_index = no_of_missions -1
        
        if budgets[previous_mission_index] <= allocated_budget:
            
            include = values[previous_mission_index] + self.find_maximum_profit(budgets, values, allocated_budget-budgets[previous_mission_index], previous_mission_index)
            exclude = self.find_maximum_profit(budgets, values, allocated_budget, previous_mission_index)
            self.mission_value_matrix[no_of_missions][allocated_budget] = max(include,exclude) 
        
            return self.mission_value_matrix[no_of_missions][allocated_budget]
        
        elif budgets[previous_mission_index] > allocated_budget:       
            self.mission_value_matrix[no_of_missions][allocated_budget] = self.find_maximum_profit(budgets, values, allocated_budget, previous_mission_index)     
            return self.mission_value_matrix[no_of_missions][allocated_budget]
        
    """
        This function is to write the output to the file(with path) given as argument          
    """   
    def write_output(self,output_file_name):
        file_handle = None
        
        try:
            lines = self.prepare_output()
            file_handle=open(output_file_name,'wt')        
            file_handle.writelines(lines)
            file_handle.flush()
        except Exception as ex :
            print('Error in writing output file to disk ',sys.exc_info())
        finally:
            if file_handle != None:
                file_handle.close()
    
    def prepare_output(self):
        
        # Initializing remaining budget after selected missions with allocated_budget
        self.remaining_budget = self.allocated_budget
        itemNo = self.no_of_missions        
        self.total_value = self.mission_value_matrix[itemNo][self.allocated_budget] if self.mission_value_matrix[itemNo][self.allocated_budget] >=0 else 0
        current_profit = self.total_value
        self.selected_missions = []

        while itemNo > 0:
            if (itemNo == 1 or current_profit != self.mission_value_matrix[itemNo-1][self.remaining_budget]) and self.budgets[itemNo-1] < self.remaining_budget: #item was included
                self.selected_missions = [itemNo] + self.selected_missions
                self.remaining_budget = self.remaining_budget - self.budgets[itemNo-1] #subtract the capacity 
                current_profit = current_profit - self.values[itemNo-1]
            itemNo = itemNo - 1

        self.selected_missions = [str(self.missions[mission_index-1]) for mission_index in self.selected_missions]
        selected_missions = ",".join(self.selected_missions)
        #print("The missions that should be funded: {0}".format(str (myList)))
        line1 = "The missions that should be funded: {0}".format(selected_missions)
        line2 = "\nTotal value: {0}".format(self.total_value)
        line3 = "\nBudget remaining: {0}".format(self.remaining_budget)
        
        return [line1, line2, line3]
        

# Actual main function to call ISROMissionApprover class and get solution
def main():   
    try:
        obj = ISROMissionApprover("inputPS8.txt",100)
        obj.total_value = obj.find_maximum_profit(obj.budgets,obj.values,obj.allocated_budget,obj.no_of_missions)
        obj.write_output("outputPS8.txt")
    except Exception as e:
        print('Something went wrong while executing the program',sys.exc_info())
    
        
if __name__ == '__main__':
    main()
