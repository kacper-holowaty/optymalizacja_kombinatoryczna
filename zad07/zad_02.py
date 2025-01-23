import pulp as pl

model = pl.LpProblem(name="Głosy w rejonie", sense=pl.LpMinimize)

x1 = pl.LpVariable('x1', lowBound=0)
x2 = pl.LpVariable('x2', lowBound=0)
x3 = pl.LpVariable('x3', lowBound=0)
x4 = pl.LpVariable('x4', lowBound=0)

model += x1 + x2 + x3 + x4


model += -2 * x1 + 8 * x2 + 0 * x3 + 10 * x4 >= 50, 'Biały'
model += 5 * x1 + 2 * x2 + 0 * x3 + 0 * x4  >= 100, 'Czerwony'
model += 3* x1 - 5 * x2 + 10 * x3 - 2 * x4 >= 25, 'Niebieski'

status = model.solve()

if pl.LpStatus[status] == "Optimal":
    print("Wartości zmiennych:")
    for variable in model.variables():
        print(f"{variable.name} = {variable.varValue}")

    print(f"Wartość funkcji celu: {pl.value(model.objective)}")
else:
    print("Model nie znalazł optymalnego rozwiązania.")