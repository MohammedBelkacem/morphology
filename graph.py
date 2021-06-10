import matplotlib.pyplot as plt

import networkx as nx
import numpy as np
import pylab

G = nx.MultiDiGraph()
#list of kabyle tags
tags=[]
i=0
#extraction du tableau des tags

for ligne in open("tagspos.txt",encoding='utf-8'):
     a=ligne.replace('\n',"")
     if (i!=0):
      b=(a,0,())
      tags.append(b)
     i=i+1

edges=[]    # Edges list
#this function renders the tag index in the tags kab array
def index_of_tag(tag):
    l=0
    while l< len(tags):
        c= tags[l]
        b=c[0]
        if (tag==b):
            return (l)
        l=l+1


regexp ='[-A-Zḍčǧḥṛṣẓṭţɣɛ« ».,:1-9a-z]+/[A-Z]+' # regular expression to retreive the couple (tagged wor/tag)

text=""
#Construction du texte global
first=0
number_of_sentences=0
stop=1 # limiter le graphe aux stop premières phrases
for ligne in open("corpus2-kab.txt",encoding='utf-8'):
     text.replace("\ufeff","")
     text=text+' '+ligne.strip()
     number_of_sentences=number_of_sentences+1
     if number_of_sentences== stop:
        break


text=text.strip().replace('\n'," ").replace("  "," ").replace("   "," ").replace("\ufeff","")
a=text.split(" ")
i=0
start=0
b=''
while i<len(a)-1:
    iii=b
    #récupérer la paire mot tag
    b=a[i].split("/")  #split a couple
    #print (b[1])

    tuplea=tags[index_of_tag(b[1])] #look for the index of the tag
    #print (tuple)
    number=tuplea[1]+1#increment the tag count
    tuple_tag=tuplea[2]
    list_a=list(tuple_tag)

    if b[1]=='NMP':
        list_a.append(b[0])
    else:
        list_a.append(b[0].lower())
    #print  (list_a)
    tuple_tag=tuple(list_a)
    tags[index_of_tag(b[1])]=(tuplea[0],number,tuple_tag)# update une tag count
    c=a[i+1].split("/") # this is for the last couple word/tag
    if(start==0) and (i==0): # the first start edge : First word in the text or the first edge after a dot
        G.add_edges_from([('Start',b[1])], weight=0)
        edges.append(('Start->'+b[1],1))
        G.add_edges_from([(b[1],c[1])], weight=0) # and create an edge betwen the dot and the previous tags
        edges.append((b[1]+'->'+c[1],1))

        start=1
        #print ('start')
    elif (start==0):

         G.add_edges_from([('Start',c[1])], weight=0) # edge start -> next word after a dot .
         start=1
         edges.append(('Start->'+c[1],1))


    elif (c[1]=='.') or (c[1]=='!') or(c[1]=='?') :

        G.add_edges_from([(c[1],'Stop')], weight=0) # when a dot is found, create an end
        edges.append((c[1]+'->Stop',1))
        G.add_edges_from([(b[1],c[1])], weight=0) # and create an edge betwen the dot and the previous tags
        edges.append((b[1]+'->'+c[1],1))
        start=0



    else:
        G.add_edges_from([(b[1],c[1])], weight=0) # create and edge between two neighbours
        edges.append((b[1]+'->'+c[1],1))

    i=i+1

# this is for the last tag. We will increment its occurence

tuplea=tags[index_of_tag(c[1])]

number=tuplea[1]+1
tuple_tag=tuplea[2]
list_a=list(tuple_tag)
list_a.append(c[0])
tuple_tag=tuple(list_a)
tags[index_of_tag(c[1])]=(tuplea[0],number,tuple_tag)

#print (tags)
val_map = {}
values = [val_map.get(node, 0.45) for node in G.nodes()]
edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])

red_edges = [('Start','NMC'),('NMC','Stop')]
edge_colors = ['black' if not edge in red_edges else 'black' for edge in G.edges()]

pos=nx.spring_layout(G)

options = {
    'node_color': 'blue',
    'node_size': 800,
    'width': 1,
    'arrowstyle': '-|>',
    'arrowsize': 13,
}
color_map = []
j=0
for node in G:
    #print (node)

    if str(node) =='Start' or str(node) =='Stop':
        color_map.append('blue')

    elif (len(str(node))>=4):
        color_map.append('olive')
    elif (len(str(node))==3):
        color_map.append('yellow')
    elif (len(str(node))==2):
        color_map.append('purple')
    else:
        color_map.append('red')
    j=j+1
nx.draw(G,pos, node_color = color_map, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
#nx.draw_networkx_labels()
#networkx.draw_networkx_labels(graph,node_positions,font_size=16)
#nx.coloring.greedy_color(G, strategy='largest_first')
#nx.draw_networkx(G, arrows=True, **options)
#print (words)i
j=0
labels={}
for i in G.nodes:

    labels[i]=i

nx.draw_networkx_labels(G,pos,labels,font_size=16)

pylab.axis('off')
pylab.savefig('demo.png', transparent=True)
pylab.show()