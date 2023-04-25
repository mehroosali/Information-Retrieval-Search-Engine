from clustering import Clustering
from pysolr import Solr
import random
from urllib.parse import urlparse

solr_url_local = 'http://localhost:8983/solr/nutch'
solr_url_ec2 = 'http://ec2-44-195-249-49.compute-1.amazonaws.com:8983/solr/nutch'

class Testing:
    def __init__(self):
        # self.queries = ["chocolate cake"]
        self.queries = ["chocolate cake", "apple pie", "cheesecake", "vanilla icecream", "Doughnuts", "waffle", "indian sweets", 
                        "Gelato", "Croissant", "carrot cake", "vanilla milkshake", "Bread pudding", "Frozen custard", "Quindim",
                        "tart", "pumpkin pie", "Brownies", "homemade Biscuits", "Popsicles", "cake receipe", "black forest cake", 
                        "Italian cakes", "red velvet cake", "cupcake", "Caramel Popcorn", "muffin", "Cookies", "Candies", "fruit salad",
                            "Chocolate sweets", "Jelly", "chocolate milkshake", "Slushies", "Sherbet", "chocolate mousse", "yogurt", "gulab jamun", 
                            "Jalebi", "blueberry muffin", "cinnamon rolls", "gingersnaps", "ice cream sundae", "key lime pie", 
                            "panna cotta", "peanut butter cookie", "Praline", "Sorbet", "Souffle", "Truffle", "Oreo", "Pecan Pie", 
                            "Banana pudding", "Baked Alaska", "Buckeyes", "S'mores", "Bananas foster", "Swiss roll", "shave ice", "churro", "tiramisu"]
        self.cluster = Clustering()
        self.solr = Solr(solr_url_ec2, always_commit=True)

    def get_urls_from_result(self, results):
        urls = []
        for result in results:
            urls.append(result['url'])  
        return urls[:15]

    def execute(self):

        for count, query in enumerate(self.queries):
            solr_query = "text:" + "\"" + query.lower() 
            solr_query += "\""
            print(solr_query)
            solr_results = self.get_results_from_solr(solr_query)
            flat_cluster_results = self.cluster.flat_Clustering(query, solr_results)
            single_cluster_results = self.cluster.hierarchical_clustering_single(query, solr_results)
            average_cluster_results = self.cluster.hierarchical_clustering_average(query, solr_results)

            file_name = "./output/query_result_"+ str(count) +".txt"
            with open(file_name, "w") as f:
                line = "Query: " + query + "\n\nSolr Results\n"
                f.write(line)
                for url in self.get_urls_from_result(solr_results):
                    f.write(str(url)+"\n")
                
                f.write("\n\nFlat Clustering Results: \n")
                for url in self.get_urls_from_result(flat_cluster_results):
                    f.write(str(url)+"\n")
                
                f.write("\nSingle Hierarchial Clustering Results: \n")
                for url in self.get_urls_from_result(single_cluster_results):
                    f.write(url + "\n")

                f.write("\nAverage Hierarchial Clustering Results: \n")
                for url in self.get_urls_from_result(average_cluster_results):
                    f.write(url + "\n")
    
    def randomize_result(self, results):
        batch_size = 10
        new_results = results[:2]

        for idx in range(2, len(results), batch_size):
            data = results[idx: idx + batch_size]
            random.shuffle(data)
            new_results.extend(data)

        return new_results

    def get_domain(self, url):
        return urlparse(url).netloc
    
    def get_results_from_solr(self, query):
        num_rows = 50
        curr_count = 0
        while curr_count < 50:
            solr_response = self.solr.search(query, search_handler="/select", **{
                "wt": "json",
                "rows": num_rows
            })
            solr_results = [result for result in solr_response]

            if num_rows > 10000:
                return self.randomize_result(solr_results)
            if len(solr_results) < 50:
                return self.randomize_result(solr_results)

            elements = {}
            new_results = []
            for res in solr_results:
                if res['url'] != '':
                    domain = self.get_domain(res['url'])
                    if domain in elements and elements[domain] < 4:
                        new_results.append(res)
                        elements[domain] += 1
                    elif domain not in elements:
                        elements[domain] = 1
                        new_results.append(res)
            curr_count = len(new_results)
            #print(f"Curr Count: {curr_count}")

            if curr_count >= 50:
                return self.randomize_result(new_results[:50])
            
            num_rows *= 2
        return self.randomize_result(solr_results)
    
test = Testing()
test.execute()