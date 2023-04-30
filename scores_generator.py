import json

#page_rank_dict = {}
rm_scores = {}
authority_scores = {}
hubs_scores = {}
# with open('page_rank_scores.txt', 'r') as file:
#     for line in file:
#         line_arr = line.split('\t')
#         url, score = line_arr[0], float(line_arr[1].strip())
#         page_rank_dict[url] = score
    
with open('rm_scores.txt', 'r') as file:
    rm_scores = json.load(file)
    
with open('authorities_scores.txt', 'r') as file:
    authority_scores = json.load(file)    

with open('hub_scores.txt', 'r') as file:
    hubs_scores = json.load(file) 

new_scores = {}
# for url, score in rm_scores.items():
#     pr_score = page_rank_dict.get(url, 0)
#     if score == 0 and pr_score == 0:
#         new_scores[url] = 0
#     elif score == 0 and pr_score != 0:
#         new_scores[url] = pr_score
#     elif score != 0 and pr_score == 0:
#         new_scores[url] = score
#     else: 
#         new_scores[url] = score*pr_score
  
for url, score in rm_scores.items():
    auth_score = authority_scores.get(url, 0)
    hubs_score = hubs_scores.get(url, 0)
    
    if score == 0:
        new_scores[url] = auth_score + hubs_score
    else: 
        new_scores[url] = score * (auth_score + hubs_score)
    
print(len(new_scores))

# print('Writing new PR scores..')    
# with open('pr_modified_scores.txt', 'w') as convert_file:
#     convert_file.write(json.dumps(new_scores))

print('Writing new HITS scores..')    
with open('hits_scores.txt', 'w') as convert_file:
    convert_file.write(json.dumps(new_scores))