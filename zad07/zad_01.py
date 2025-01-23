import pulp as pl

model = pl.LpProblem(name="Wydatki Oli", sense=pl.LpMinimize)

x1 = pl.LpVariable('x1', lowBound=0)
x2 = pl.LpVariable('x2', lowBound=0)
x3 = pl.LpVariable('x3', lowBound=0)
x4 = pl.LpVariable('x4', lowBound=0)
x5 = pl.LpVariable('x5', lowBound=0)

model += 0.15 * x1 + 0.5 * x2 + 0.15 * x3 + 1.2 * x4 + 0.08 * x5

model += x1 + x2 + x3 + x4 + x5 <= 20, 'Porcja dzienna'

model += 3 * x1 + 38 * x2 + 20 * x4 + x5 >= 70, 'Białko'
model += 140 * x1 + 120 * x2 + 5760 * x5 >= 5000, 'Witamina A'
model += x1 + 3 * x5 >= 75, 'Witamina C'
model += 120 * x1 + 1450 * x2 + 90 * x3 + 8 * x4 + 19 * x5 >= 70, 'Wapń'
model += 53 * x1 + 200 * x2 + 240 * x3 + 82 * x4 + 21 * x5 >= 2700, 'kcal'

status = model.solve()

# Niemożliwe do rozwiązania.