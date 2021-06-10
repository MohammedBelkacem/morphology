import networkx as nx
graph = nx.DiGraph()

sentence = "Yerna/VP -d/PDS ussan/NMC -agi/PAN i?eddan/VPPP yiwen/NC n/PP udlis/NMC n/PP tmazi?t/NMC ,/, d/PREAL ayen/PRI ara/PRPT d-/PDP yernun/VPA aba?ur/NMC i/PRP tutlayt/NMC -agi/PAN n/PP tyemmat/NMC ./."
tokens=sentence.split(" ")
j=0
previous=""
couples=[]
while j<len(tokens):
    if previous !="":

        couple=(previous,tokens[j].split("/")[1])
        previous=tokens[j].split("/")[1]
        couples.append(couple)

    else:
        previous=tokens[j].split("/")[1]
    j=j+1

print(couples)
graph.add_edges_from(couples)
#nx.is_directed(graph) # => True
from matplotlib import pyplot as plt
plt.tight_layout()
nx.draw_networkx(graph, arrows=True)
plt.savefig("g1.png", format="PNG")
plt.show()