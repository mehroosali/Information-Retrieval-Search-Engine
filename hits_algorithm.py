import networkx as nx
import json

inlinks_dict = {}
outlinks_dict = {}

#Generating the inlinks_dict from inlinks_webgraph
with open("results/inlinks_webgraph", encoding="utf8") as inlink_file:
    for line in inlink_file:
        if line.strip():  # checks if line is not empty or contains only whitespaces
            if "Inlinks" in line:
                d_key = line.split("\t")[0]
                d_value = []
            elif "fromUrl" in line:
                d_value.append(line.split()[1])
        else:
            if d_value:  # checks if d_value is not empty before adding to dictionary
                inlinks_dict[d_key] = d_value

#Generating the outlinks_dict from inlinks_dict
for key, value in inlinks_dict.items():
    for url in value:
        outlinks_dict.setdefault(url, []).append(key)

print('HITS Algorithm started..')
G = nx.Graph(outlinks_dict)
hubs, authorities = nx.hits(G, max_iter=10000, normalized=True)
print('HITS Algorithm ended..')

hubs_sorted = dict(sorted(hubs.items(), key=lambda x:x[1], reverse=True))
authorities_sorted = dict(sorted(authorities.items(), key=lambda x:x[1], reverse=True))

with open('hub_scores.txt', 'w') as convert_file:
    convert_file.write(json.dumps(hubs_sorted))

with open('authorities_scores.txt', 'w') as convert_file:
    convert_file.write(json.dumps(authorities_sorted))



