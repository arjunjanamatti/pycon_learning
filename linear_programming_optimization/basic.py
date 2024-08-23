import pulp

# create the LP problem
lp_problem = pulp.LpProblem("apples and candy bars", pulp.LpMaximize)

# define the decision variables
apples = pulp.LpVariable('apples', lowBound=0)
candy_bars = pulp.LpVariable('candy_bars', lowBound=0)

# add the objective function - level of enjoyment from specific diet
# notice no equality or inequality at the end of the function
lp_problem += 1 * apples + 3 * candy_bars

# add calorie constraint
lp_problem += 95*apples + 215*candy_bars <= 850
# add sugar constraint
lp_problem += 15*apples + 20*candy_bars <= 100

# solve the problem
lp_problem.solve()

# printing the results
print(f"Status: {pulp.LpStatus[lp_problem.status]}")
print(f"apples = {pulp.value(apples)}")
print(f"candy_bars = {pulp.value(candy_bars)}")
print(f"Objective value: {pulp.value(lp_problem.objective)}")
