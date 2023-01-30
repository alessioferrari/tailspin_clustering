'''
Created on 06/lug/2011

@author: alessio
'''
import os
import nltk


class XMLReqClusterSet(object):
    """
    This class represent a requirements cluster set: given a folder
    this class build a list for each file in the folder where
    each element of the list is a line of the file. 
    Each list will be consider as a requirements cluster
    """
    
    def __init_list(self, in_file, o_sorted_id):
        """
        Scans the file in_file and returns a sorted list of requirements ID (numeric) 
        contained in the file
        """
        l_raw = in_file.read()
        l_tokens = nltk.line_tokenize(l_raw)
        for l_token in l_tokens:
            o_sorted_id.append(int(l_token.split()[0]))

    def __init_outliers(self, max_id_value):
        """
        This function checks and save all the ids that are not contained in 
        any of the clusters found
        """
        l_evaluation_id_list = [None]*(max_id_value + 1)
    
        l_id_list_numeric = [r_id for cluster in self.__cluster_id_list_numeric for r_id in cluster]
        for ids in l_id_list_numeric:
                    l_evaluation_id_list[int(ids)] = ids
           
        #print all the requirements ID that have not been clustered
        unclustered_requirements_id = list()
        for i, ids in enumerate(l_evaluation_id_list):
            if i != 0 and ids == None:
                unclustered_requirements_id.append(i)
        
        return unclustered_requirements_id

    def __init__(self, in_folder_name, algorithm, max_id_value, distance_type):
        """
        Given the folder the constructor associates
        each file of the folder to a cluster and loads
        the ids contained in the folder
        @param: algorithm can be 'wcc' or 'tailspin'
        @param distance_type: jaccard-terms, lev-terms, jaccard-pos, jaccard-lev-terms, combo
        """
        listing = os.listdir(in_folder_name)
        self.__cluster_dir = in_folder_name
        self.__cluster_id_list_numeric = list()
        self.__algorithm = algorithm
        self.__distance_type = distance_type
    
        for infile in listing:
                l_input_f = open(in_folder_name + infile, "r")
                l_id_list_numeric = list()
                self.__init_list(l_input_f, l_id_list_numeric)         
                l_input_f.close()
                self.__cluster_id_list_numeric.append(l_id_list_numeric)
        
        self.__outliers = self.__init_outliers(max_id_value)
        if algorithm == 'wcc':
            self.__threshold = in_folder_name.split('/')[-2].split('-')[-1]
            self.__windowsize = None 
            self.__lookahead = None
        elif algorithm == 'tailspin':
            self.__threshold = in_folder_name.split('/')[-2].split('-')[-3]
            self.__windowsize = in_folder_name.split('/')[-2].split('-')[-2]
            self.__lookahead = in_folder_name.split('/')[-2].split('-')[-1]
        
    
    def get_clusters_dir(self):
        return self.__cluster_dir
    
    def get_clusters(self):
        """
        This function returns a list of lists, where each sub-list
        contains the id of a cluster
        """
        clusters = self.__cluster_id_list_numeric    
        return clusters 
    
    def get_cluster_num(self):
        return len(self.__cluster_id_list_numeric)
    
    def get_outliers_num(self):
        return len(self.__outliers)   
    
    def get_outliers(self):
        """
        This function returns a list of ids that represent the outliers
        of a cluster set
        """
        outliers = self.__outliers
        return outliers
    
    def get_clusters_threshold(self):
        """ 
        returns the threshold used to perform this clustering 
        (currently deduced from the folder name)
        """
        return self.__threshold
    
    def get_clusters_window(self):
        return self.__windowsize
    
    def get_clusters_look_ahead(self):
        return self.__lookahead
    
    def get_cluster_by_id(self, c_id):
        """
        This function returns the cluster with id equals to the cluster id
        """
        if c_id > 0 and c_id < len(self.__cluster_id_list_numeric):
            return self.__cluster_id_list_numeric[c_id-1]
        
        return None
    
    def get_cluster_distance_type(self):
        return self.__distance_type
    
    def get_silhouette(self, similarity_file):
        """
        This function returns the silhouette value of the cluster set,
        given the location of the file containing the similarities
        """
        
            
#x = XMLReqClusterSet('clusters/clusters-jaccard-pos/2007-ertms-clusters-04/', 205)
#print x.get_outliers()
#print x.get_clusters()
#print x.get_cluster_num()
#print x.get_cluster_by_id(1)
        
        