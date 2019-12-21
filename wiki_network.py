import requests
import networkx as nx
import pandas as pd
import numpy as np
import itertools as IT
from time import sleep
PYTHONIOENCODING="UTF-8"

timestamp = ["2015-08-31T00:00:00Z"]
titles = 'Artificial intelligence'
path = 'wiki_2015_month/201508/'

## collect hyperlinks related with article on given titles at given timestamp and save it as .csv
def get_link (titles, timestamp,path):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": titles,
        "prop": "revisions",
        "rvlimit" : 1,
        "rvprop" : "ids",
        "rvdir" : "older",
        "rvstart" : timestamp
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    pageid = list(DATA['query']['pages'].keys())[0] #page id for Augmented_reality
    if 'revisions' in DATA['query']['pages'][pageid].keys():
        revid =DATA['query']['pages'][pageid]['revisions'][0]['revid']  #180468454
        S2 = requests.Session()
        PARAMS = {
            "action": "parse",
            "format": "json",
            "oldid" : revid, #revision id
            "prop" : "links",
            "pllimit" : 1000
            }
        R2 = S.get(url=URL, params=PARAMS)
        DATA = R2.json()
        link_revid = []
        for i in DATA['parse']['links']:
            link_revid.append(i['*'])
        link_revid = pd.DataFrame(link_revid)
        link_revid['source'] = titles
        link_revid.columns=['target','source']
        link_revid = link_revid[['source', 'target']]
        link_revid=link_revid[~link_revid.target.str.contains(":")]
        link_revid=link_revid[~link_revid.source.str.contains(":")]
        titles = titles.replace('/','')
        link_revid.to_csv(path + str(titles) + '_' + timestamp.split('-')[0] +timestamp.split('-')[1] + '.csv')

## collect hyperlinks related with article on given titles at given timestamp and return it as edgelist
def get_link_df (titles, timestamp):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": titles,
        "prop": "revisions",
        "rvlimit" : 1,
        "rvprop" : "ids",
        "rvdir" : "older",
        "rvstart" : timestamp
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    pageid = list(DATA['query']['pages'].keys())[0] #page id for Augmented_reality
    if 'revisions' in DATA['query']['pages'][pageid].keys():
        revid =DATA['query']['pages'][pageid]['revisions'][0]['revid']  #180468454
        S2 = requests.Session()
        PARAMS = {
            "action": "parse",
            "format": "json",
            "oldid" : revid,
            "prop" : "links",
            "pllimit" : 1000
            }
        R2 = S.get(url=URL, params=PARAMS)
        DATA = R2.json()
        link_revid = []
        for i in DATA['parse']['links']:
            link_revid.append(i['*'])
        link_revid = pd.DataFrame(link_revid)
        if link_revid.shape[1] != 0:
            link_revid['source'] = titles
            link_revid.columns=['target','source']
            link_revid = link_revid[['source', 'target']]
            link_revid=link_revid[~link_revid.target.str.contains(":")]
            link_revid=link_revid[~link_revid.source.str.contains(":")]
            titles = titles.replace('/','')
            return link_revid


## save level_1 network
for i in timestamp:
    res = get_link(titles,i,path)

## save level_2 network
i=timestamp[0]

level_one = pd.read_csv(path + titles + '_' + i.split('-')[0] +i.split('-')[1]+ '.csv')
level_one = level_one.drop(columns = 'Unnamed: 0')

one_hop = {}

for j in level_one['target']:
    one_hop[j] = get_link_df(j, i)

level_two = pd.DataFrame(columns=['source', 'target'])
for m in one_hop.keys():
    level_two = pd.concat([level_two,one_hop[m]])

df_for_node = pd.concat([level_one, level_two])

df_for_node_reverse = df_for_node[['target','source']]
df_for_node_reverse = df_for_node_reverse.rename(columns={"target": "source", "source": "target"})
df_for_node = pd.concat([df_for_node, df_for_node_reverse])
df_for_node = df_for_node.drop_duplicates()
level_two_graph = nx.from_pandas_edgelist(df_for_node, source = 'source', target = 'target')
print(nx.is_connected(level_two_graph))
df_for_node.to_csv(path+"AI_wikipedia_twohop_network" + "_" + i.split('-')[0] + i.split('-')[1] + '.csv')

i=timestamp[0]
### read level_two_network and generate level_three_network
df_for_node = pd.read_csv(path+"AI_wikipedia_twohop_network" + "_" + i.split('-')[0] + i.split('-')[1] + '.csv')
df_for_node = df_for_node.drop(columns = 'Unnamed: 0')
g = nx.from_pandas_edgelist(df_for_node, source='source', target='target')
print(nx.is_connected(g))
level_two = df_for_node[df_for_node.source != 'Artificial intelligence']

level_two_node = level_two['target'].unique()

target = {}
for tgt in level_two_node[26282:]:
    try:
        target[tgt] = get_link_df(tgt,i)
        print(tgt+' collected')
    except KeyError:
        print('keyerror but continue')
        sleep(5)
        continue

whole = pd.DataFrame(columns = ['source','target'])

for hop in target.keys():
    whole = pd.concat([whole, target[hop]])
level_three = pd.concat([df_for_node, whole])
g = nx.from_pandas_edgelist(level_three, source='source', target='target')
print(nx.is_connected(g))

level_three.to_csv(path+titles+"_"+i.split('-')[0]+i.split('-')[1]+"level_three_.csv")

##calculate node and edge number
import pandas as pd
import networkx as nx
one = pd.read_csv('Artificial intelligence_201712.csv')
two = pd.read_csv('AI_wikipedia_twohop_network_201712.csv')
three = pd.read_csv('Artificial intelligence_201712level_three_.csv')

level_one = set(one['target'])
level_two = set(two['target'])

level_one = list(level_one)
level_two = list(level_two)

node = level_one + level_two
node = list(set(node))
three = three[three['source'].isin(node)]
three = three[three['target'].isin(node)]

three = three.drop(columns = 'Unnamed: 0')
three_reverse = three[['target','source']]
three_reverse = three_reverse.rename(columns={"target": "source", "source": "target"})
three = pd.concat([three, three_reverse])
three = three.drop_duplicates()
three.shape
three.to_csv('')

##select only rows containing string 'technology'
df1 = three
df1['source'] = df1['source'].replace({'Artificial intelligence':'Artificial intelligence technology'})
df1['target'] = df1['target'].replace({'Artificial intelligence':'Artificial intelligence technology'})

df1=df1[df1['source'].str.contains('technology', regex=False,na = False)]
df1=df1[df1['target'].str.contains('technology', regex=False, na = False)]


g = nx.from_pandas_edgelist(three, source='source', target='target')
print(nx.density(g))
