import pickle
class Clustering:
    def __init__(self):
        self.url_clusterNum_flat = {}
        self.url_clusterNum_single = {}
        self.url_clusterNum_average = {}
        self.cluster_center_flat = {}
        self.cluster_center_single = {}
        self.cluster_center_average = {}
        self.tfidf = pickle.load(open("./results/tfidfVec.pickle", "rb"))
        self.read_URL_cluster_flat()
        self.read_cluster_center_flat()
        self.read_URL_cluster_average()
        self.read_cluster_center_average()
        self.read_URL_cluster_single()
        self.read_cluster_center_single()
        
    
    def read_URL_cluster_flat(self):
        with open("./results/url_cluster_flat.txt", "r") as f:
            while line := f.readline():
                url, cluster_num = line.strip().split(" ")
                self.url_clusterNum_flat[url] = cluster_num

    def read_cluster_center_flat(self):
        with open("./results/cluster_center_flat.txt", "r") as f:
            while line := f.readline():
                data = line.strip().split(" ")
                center = int(data[0])
                value = " ".join(data[1:])[1:-1]
                center_coordinate = [float(c) for c in value.split(",")]
                self.cluster_center_flat[int(center)] = center_coordinate
    
    def read_cluster_center_average(self):
        with open("./results/cluster_center_hac_avg.txt", "r") as f:
            while line := f.readline():
                data = line.strip().split(" ")
                center = int(data[0])
                value = " ".join(data[1:])[1:-1]
                center_coordinate = [float(c) for c in value.split(",")]
                self.cluster_center_average[int(center)] = center_coordinate
    
    def read_URL_cluster_average(self):
        with open("./results/url_cluster_hac_avg.txt", "r") as f:
            while line := f.readline():
                url, cluster_num = line.strip().split(" ")
                self.url_clusterNum_average[url] = cluster_num
    
    def read_cluster_center_single(self):
        with open("./results/cluster_center_hac_single.txt", "r") as f:
            while line := f.readline():
                data = line.strip().split(" ")
                center = int(data[0])
                value = " ".join(data[1:])[1:-1]
                center_coordinate = [float(c) for c in value.split(",")]
                self.cluster_center_single[int(center)] = center_coordinate
    
    def read_URL_cluster_single(self):
        with open("./results/url_cluster_hac_single.txt", "r") as f:
            while line := f.readline():
                url, cluster_num = line.strip().split(" ")
                self.url_clusterNum_single[url] = cluster_num

    def euclidean_distance(self, list1, list2):
        squares = [(p-q) ** 2 for p, q in zip(list1, list2)]
        return sum(squares) ** .5

    def get_Query_weight(self, query):
        weight = self.tfidf.transform([query])
        arr = weight.toarray().tolist()
        return arr[0]

    def compute_distance(self, query, type):
        query_weight = self.get_Query_weight(query)
        results = []
        if type == 'flat':
            for cluster_num, center in self.cluster_center_flat.items():
                distance = self.euclidean_distance(center, query_weight)
                results.append((cluster_num, distance))
        elif type == 'average':
            for cluster_num, center in self.cluster_center_average.items():
                distance = self.euclidean_distance(center, query_weight)
                results.append((cluster_num, distance))
        else:
            for cluster_num, center in self.cluster_center_single.items():
                distance = self.euclidean_distance(center, query_weight)
                results.append((cluster_num, distance))
        
        results.sort(key = lambda item: (item[1], item[0]))
        return_val = [item[0] for item in results]

        return return_val

    def flat_Clustering(self, query, results):
        sorted_clusters = self.compute_distance(query, 'flat')
        values = {}
        not_imp_urls = []
        for res in results:
            url = res['url']
            if url in self.url_clusterNum_flat:
                cluster_num = int(self.url_clusterNum_flat[url])
            else:
                not_imp_urls.append(res)
        
            if cluster_num in values:
                values[cluster_num].append(res)
            else:
                values[cluster_num] = [res]
        
        new_results = []
        for cluster_num in sorted_clusters:
            if cluster_num in values:
                new_results.extend(values[cluster_num])

        new_results.extend(not_imp_urls)
        return new_results

    def hierarchical_clustering_average(self, query, results):
        sorted_clusters = self.compute_distance(query, 'average')
        values = {}
        not_imp_urls = []
        for res in results:
            if res['url'] in self.url_clusterNum_average:
                cluster_num = int(self.url_clusterNum_average[res['url']])
            else:
                not_imp_urls.append(res)
                continue

            if cluster_num in values:
                values[cluster_num].append(res)
            else:
                values[cluster_num] = [res]
        
        new_results = []

        for cluster_num in sorted_clusters:
            if cluster_num in values:
                new_results.extend(values[cluster_num])

        new_results.extend(not_imp_urls)
        return new_results
    

    def hierarchical_clustering_single(self, query, results):
        sorted_clusters = self.compute_distance(query, 'single')
        values = {}
        not_imp_urls = []
        for res in results:
            if res['url'] in self.url_clusterNum_single:
                cluster_num = int(self.url_clusterNum_single[res['url']])
            else:
                not_imp_urls.append(res)
                continue

            if cluster_num in values:
                values[cluster_num].append(res)
            else:
                values[cluster_num] = [res]
        
        new_results = []
        for cluster_num in sorted_clusters:
            if cluster_num in values:
                new_results.extend(values[cluster_num])

        new_results.extend(not_imp_urls)
        return new_results