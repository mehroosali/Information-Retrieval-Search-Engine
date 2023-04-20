import pickle
class Clustering:
    def __init__(self):
        self.url_clusterNum_flat = {}
        self.cluster_center_flat = {}
        self.cluster_center_hac = {}
        self.url_clusterNum_hac = {}
        self.tfidf = pickle.load(open("./results/tfidfVec.pickle", "rb"))
        self.read_URL_cluster_flat()
        self.read_cluster_center_flat()
        self.read_URL_cluster_hac()
        self.read_cluster_center_hac()
        
    
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
    
    def read_cluster_center_hac(self):
        with open("./results/cluster_center_hac.txt", "r") as f:
            while line := f.readline():
                data = line.strip().split(" ")
                center = int(data[0])
                value = " ".join(data[1:])[1:-1]
                center_coordinate = [float(c) for c in value.split(",")]
                self.cluster_center_hac[int(center)] = center_coordinate
    
    def read_URL_cluster_hac(self):
        with open("./results/url_cluster_hac.txt", "r") as f:
            while line := f.readline():
                url, cluster_num = line.strip().split(" ")
                self.url_clusterNum_hac[url] = cluster_num

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
        else:
            for cluster_num, center in self.cluster_center_hac.items():
                distance = self.euclidean_distance(center, query_weight)
                results.append((cluster_num, distance))
        
        results.sort(key = lambda item: (item[1], item[0]))
        return_val = [item[0] for item in results]

        return return_val

    def flat_Clustering(self, query, results):
        sorted_clusters = self.compute_distance(query, 'flat')
        values = {}
        for res in results:
            url = res['url']
            if url in self.url_clusterNum_flat:
                cluster_num = int(self.url_clusterNum_flat[url])
            else:
                print("URL Doesn't exists in collection.")
                return results
            if cluster_num in values:
                values[cluster_num].append(res)
            else:
                values[cluster_num] = [res]
        
        new_results = []
        for cluster_num in sorted_clusters:
            if cluster_num in values:
                new_results.extend(values[cluster_num])
        return new_results

    def hierarchical_clustering(self, query, results):
        sorted_clusters = self.compute_distance(query, 'flat')
        values = {}
        clusters_numbers = []
        for res in results:
            if res['url'] in self.url_clusterNum_hac:
                cluster_num = int(self.url_clusterNum_hac[res['url']])
            else:
                print("URL Doesn't exists in collection.")
                return results
            if cluster_num in values:
                values[cluster_num].append(res)
            else:
                values[cluster_num] = [res]
                clusters_numbers.append(cluster_num)
        
        new_results = []

        for cluster_num in sorted_clusters:
            if cluster_num in values:
                new_results.extend(values[cluster_num])

        return new_results