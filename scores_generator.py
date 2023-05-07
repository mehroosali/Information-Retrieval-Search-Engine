import json

def generate_modified_pr_scores():
    rm_scores = {}
    page_rank_dict = {}
    new_scores = {}
    with open('results/page_rank_scores.txt', 'r') as file:
        for line in file:
            line_arr = line.split('\t')
            url, score = line_arr[0], float(line_arr[1].strip())
            page_rank_dict[url] = score
    
    with open('results/rm_scores.txt', 'r') as file:
        rm_scores = json.load(file)

    for url, score in rm_scores.items():
        pr_score = page_rank_dict.get(url, 0)
        if score == 0 and pr_score == 0:
            new_scores[url] = 0
        elif score == 0 and pr_score != 0:
            new_scores[url] = pr_score
        elif score != 0 and pr_score == 0:
            new_scores[url] = score
        else: 
            new_scores[url] = 0.3*score + 0.7*pr_score

    # max_score = max(new_scores.values())

    # for key in new_scores:
    #     new_scores[key] /= max_score 

    print('Writing new PR scores..')    
    with open('results/pr_modified_scores.txt', 'w') as convert_file:
        convert_file.write(json.dumps(new_scores))    

def generate_hits_score():
    rm_scores = {}
    new_scores = {}
    authority_scores = {}
    hubs_scores = {}
    with open('results/rm_scores.txt', 'r') as file:
        rm_scores = json.load(file)

    with open('results/authorities_scores.txt', 'r') as file:
        authority_scores = json.load(file)    

    with open('results/hub_scores.txt', 'r') as file:
        hubs_scores = json.load(file) 
  
    for url, score in rm_scores.items():
        auth_score = authority_scores.get(url, 0)
        hubs_score = hubs_scores.get(url, 0)
        
        if score == 0:
            new_scores[url] = auth_score + hubs_score
        else: 
            new_scores[url] = 0.3*score + 0.7*(auth_score + hubs_score)

    print('Writing new HITS scores..')    
    with open('results/hits_scores.txt', 'w') as convert_file:
        convert_file.write(json.dumps(new_scores))

def generate_vs_rm_scores_from_solr():
    rm_scores = {}
    with open('results/solr_data.json', encoding="utf8") as f:
        print("Loading Json file ....")
        data = json.load(f)
        print("Loaded successfully!")
        documents = data['response']['docs']
        print(f"Length of the documents: {len(documents)}")
        
        for record in documents:
            if 'url' in record:
                url = record['url']
                score = record.get('boost', 0)
                rm_scores[url] = score
                
    with open('results/rm_scores.txt', 'w') as convert_file:
        convert_file.write(json.dumps(rm_scores))
    print(len(rm_scores))

if __name__ == "__main__":
    generate_vs_rm_scores_from_solr()
    generate_modified_pr_scores()
    generate_hits_score()
