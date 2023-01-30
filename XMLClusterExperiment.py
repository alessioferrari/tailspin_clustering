'''
Created on 06/lug/2011

@author: alessio
'''

from XMLReqClusterSet import XMLReqClusterSet
import os

class XMLClusterExperiment(object):
    """
    This class embeds the elements in a clustering experiments
    """

    def __init__(self, cluster_experiment_path, expected_outliers_file, algorithm, max_id_value, distance_type):
        """
        For each folder contained in the @param cluster_experiment_path
        this function creates an XMLReqClusterSet object 
        embedding all the information about the cluster.
        It then load the list of expected outliers from the 
        @param expected_outliers_file
        @param distance_type: jaccard-terms, lev-terms, jaccard-pos, jaccard-lev-terms, combo 
        """
        self.__cluster_set = list()
        self.__algorithm = algorithm
        self.__distance_type = distance_type
        folders = os.listdir(cluster_experiment_path)
        for folder in folders:
            clusters = XMLReqClusterSet(cluster_experiment_path + os.altsep + folder + os.altsep, algorithm, max_id_value, distance_type)
            self.__cluster_set.append(clusters)

    def get_cluster_sets(self):
        """
        @return: a copy of all the clusters of the cluster set
        """
        cluster_sets = self.__cluster_set
        return cluster_sets 
    
    def get_distance_type(self):
        return self.__distance_type
    
    def get_wcc_cluster_set(self, threshold_value):  
        """
        If the algorithm adopted is wcc, this function returns the cluster set with
        threshold equals to threshold_value 
        If the algorithm adopted is different from wcc this function
        returns None
        """  
        if self.__algorithm == 'wcc':
            clusters = [c for c in self.__cluster_set if c.get_clusters_threshold() == threshold_value]
            if len(clusters) == 1:
                return clusters[0]
        
        return None
    
    def get_tailspin_cluster_set(self, threshold_value, window_size, look_ahead):
        """
        """
        if self.__algorithm == 'tailspin':
            clusters = [c for c in self.__cluster_set if c.get_clusters_threshold() == threshold_value and \
                        c.get_clusters_window() == window_size and c.get_clusters_look_ahead() == look_ahead]
            if len(clusters) == 1:
                return clusters[0]
        
        return None
    
    
#x = XMLClusterExperiment('../clusters/clusters-jaccard-pos','', 'wcc',  255)
#x = XMLClusterExperiment('../tailspin-clusters/clusters-jaccard-lev-terms','','tailspin', 205)
#print x.get_tailspin_cluster_set('04','1','3').get_clusters()
#print x.get_tailspin_cluster_set('04','1','3').get_outliers()
