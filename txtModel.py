from model.model import Model

model = Model()
graph = model.buildGraph('France', 2015)
print(graph)

path, sol = model.calcolaPercorso(5)
print(path, sol)