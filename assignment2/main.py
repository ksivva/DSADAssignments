import sys

OUTPUT_FILE_NAME = "outputPS8.txt"

INPUT_FILE_NAME = "inputPS8.txt"

WRITE_MODE = "w"

READ_MODE = "r"


def solve_knapsack(profits, weights, capacity):
    # basic checks
    n = len(profits)
    if capacity <= 0 or n == 0 or len(weights) != n:
        return 0

    dp = [[0 for x in range(capacity + 1)] for y in range(n)]

    # populate the capacity = 0 columns, with '0' capacity we have '0' profit
    for i in range(0, n):
        dp[i][0] = 0

    # if we have only one weight, we will take it if it is not more than the capacity
    for c in range(0, capacity + 1):
        if weights[0] <= c:
            dp[0][c] = profits[0]

    # process all sub-arrays for all the capacities
    for i in range(1, n):
        for c in range(1, capacity + 1):
            profit1, profit2 = 0, 0
            # include the item, if it is not more than the capacity
            if weights[i] <= c:
                profit1 = profits[i] + dp[i - 1][c - weights[i]]
            # exclude the item
            profit2 = dp[i - 1][c]
            # take maximum
            dp[i][c] = max(profit1, profit2)

    missionNumbersAndWeightsTuple = get_selected_missions_and_weights(dp, weights, profits, capacity)
    # maximum profit will be at the bottom-right corner.
    sys.stdout = open(OUTPUT_FILE_NAME, WRITE_MODE)
    print("The missions that should be funded : " + str(missionNumbersAndWeightsTuple[0]))
    print("Total Value: " + str(dp[n - 1][capacity]))
    # Subtract the sum of the budgets for all the missions selected from 100 (capacity)
    print("Budget remaining: " + str(capacity - sum(missionNumbersAndWeightsTuple[1])))
    sys.stdout.close()


# This method returns a tuple containing 2 elements:
# 1) Comma separated string of the missions that are selected
# 2) The corresponding budget for the mission
def get_selected_missions_and_weights(dp, weights, profits, capacity):
    n = len(weights)
    totalProfit = dp[n - 1][capacity]
    missionsSelected = ""
    weightsOfSelectedMissions = []
    for i in range(n - 1, 0, -1):
        if totalProfit != dp[i - 1][capacity]:
            missionsSelected = missionsSelected + str(i + 1) + ","
            weightsOfSelectedMissions.append(weights[i])
            capacity -= weights[i]
            totalProfit -= profits[i]

    if totalProfit != 0:
        weightsOfSelectedMissions.append(weights[0])
    # Removing the last ',' from the string
    missionsSelected = missionsSelected[:-1]
    missionNumbersAndWeightsTuple = (missionsSelected, weightsOfSelectedMissions)
    return missionNumbersAndWeightsTuple


def main():
    val = []
    wt = []
    W = 100
    f = open(INPUT_FILE_NAME, READ_MODE)
    lines = f.readlines()
    for line in lines:
        values = line.strip().split('/')
        if values[1].isnumeric():
            wt.append(int(values[1]))
        else:
            print("The budget is not a number. Please enter valid budget")
        if values[2].isnumeric():
            val.append(int(values[2]))
        else:
            print("The value is not numeric. Please enter valid value")

    solve_knapsack(val, wt, W)


if __name__ == '__main__':
    main()
