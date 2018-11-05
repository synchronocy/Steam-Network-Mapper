import requests
import os
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from operator import itemgetter
friends = []

G = nx.Graph();
def save(user):
    try:
        fig_size = plt.rcParams["figure.figsize"]
        if len(G.nodes()) > 30:
            fig_size[0] = str(len(G.nodes())*0.05)
            fig_size[1] = str(len(G.nodes())*0.05)
        else:
            fig_size[0] = 30
            fig_size[1] = 30
        edges = G.edges()
        colors = [G[u][v]['color'] for u,v in edges]
        plt.rcParams["figure.figsize"] = fig_size
        pos = nx.spring_layout(G,k=0.15,iterations=20)
        nx.draw(G,pos=pos, with_labels=True, edge_color=colors,nodelist=sorted(G.nodes()))
        plt.savefig(user.replace('id/','')+'.png')
        plt.show()
        sys.exit()
    except Exception:
        print('Possibly ran out of memory or an unknown error has occured.')
        sys.exit()
        
def scan(user):
    #src = requests.get(origin).text
    print('Scanning: '+user)
    src = requests.get('https://steamcommunity.com/'+user+'/friends').text
    links = src.split('href="https://steamcommunity.com/')[1:]
    for link in links:
        link = link.split('"')[0]
        link = link.replace('linkfilter/?url=http://www.geonames.org','').replace('login/home/?goto=id%2Finjewlid%2Ffriends','').replace('?subsection=broadcasts','').replace('market/','').replace('workshop/','').replace('discussions/','').replace('my/wishlist/','').replace('?subsection=broadcasts','').replace('login/home/?goto=id%2F'+user+'%2Ffriends','')
        link = link.rstrip()
        if 'login/home/?' in link:
            continue
        #print(link)
        G.add_node(link)
        if len(link) < 1:
            continue
        friends.append(link)
        G.add_edge(user, link, color='g')

def main():
    counter = 0
    user = 'id/injewlid'
    steps = 3 # Friends to search for mutual
    if steps <= 3:
        scan(user)
        while True:
            for friend in friends:
                if user == friend:
                    continue
                if '/' in friend:
                    if counter < steps: # reason being because we kept running out of memory
                        counter +=1
                        scan(friend)
                        friends.remove(friend)
                else:
                    continue
            save(user)
if __name__ == '__main__':
    main()
        
    
    
