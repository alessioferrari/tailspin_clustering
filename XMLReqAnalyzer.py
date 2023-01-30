"""
Created on 05/lug/2011

@author: alessio
"""
from XMLClusterExperiment import XMLClusterExperiment
from XMLReqManager import XMLReqManager
import os
import errno
import matplotlib
from matplotlib import pyplot
import numpy

class XMLReqAnalyzer(object):
    """
    This class performs all the operations required to analyze the 
    output coming from the analysis of a requirement file
    whose manager is given as input during construction. 
    The results of the experiment are also passed as input
    """

    def __init__(self, xml_req_manager, xml_cluster_experiment):
        self.__xrm = xml_req_manager
        self.__xce = xml_cluster_experiment
        
    def print_tailspin_cluster_experiment(self, res_path):
        """
        This function prints the requirements associated to each cluster set:
        requirements belonging to the same cluster are printed together
        while requirements belonging to different clusters are printed 
        separately
        """
        cluster_sets = self.__xce.get_cluster_sets()
        for set in cluster_sets:
            t = set.get_clusters_threshold()
            w = set.get_clusters_window()
            l = set.get_clusters_look_ahead()
            file_name = 'clusters-' + t + '-' + w + '-' + l + '.txt'
            file = open(res_path+file_name, 'w')
            title = 'CLUSTER RESULTS for tailspin algorithm threshold = ' + t + ' window = ' + w + 'lookahead = ' + l + '\n\n'
            print 'writing' + file_name
            file.write(title)
            clusters = set.get_clusters()
            for i, c in enumerate(clusters):
                file.write('cluster'+ str(i+1) + '\n')
                for line_num in c:
                    file.write(str(self.__xrm.get_requirement_id_by_line(int(line_num))) + ' ')
                    file.write(str(self.__xrm.get_requirement_text_by_line(int(line_num))) + '\n')
                file.write('\n\n')
            file.close()
            
    def print_single_tailspin_cluster_experiment(self, res_path, t_in, w_in, l_in):
        cluster_set = self.__xce.get_tailspin_cluster_set(t_in, w_in, l_in)
        file_name = 'clusters-' + t_in + '-' + w_in + '-' + l_in + '.txt'
        file = open(res_path+file_name, 'w')
        title = 'CLUSTER RESULTS for tailspin algorithm threshold = ' + t_in + ' window = ' + w_in + 'lookahead = ' + l_in + '\n\n'
        print 'writing' + file_name
        file.write(title)
        clusters = cluster_set.get_clusters()
        for i, c in enumerate(clusters):
            file.write('cluster'+ str(i+1) + '\n')
            for line_num in c:
                #file.write(str(self.__xrm.get_requirement_id_by_line(int(line_num))) + ' ')
                file.write(str(self.__xrm.get_requirement_text_by_line(int(line_num))) + '\n')
            file.write('\n\n')
        file.close()
            
    def print_cluster_num(self, fp):
        cluster_sets = self.__xce.get_cluster_sets()
        for set in cluster_sets:
            t = set.get_clusters_threshold()
            w = set.get_clusters_window()
            l = set.get_clusters_look_ahead()
            title = 'CLUSTER RESULTS for tailspin algorithm threshold = ' + t + ' window = ' + w + ' lookahead = ' + l + '\n'
            print >>fp, title
            clusters = set.get_clusters()
            outliers = 0
            for cluster in clusters:
                if len(cluster) == 1:
                    outliers = outliers + 1
            print >>fp, "number of clusters: ", len(set.get_clusters()) - outliers, '\n'
            print >>fp, "number of outliers: ", outliers, '\n'
    
    def print_tailspin_outliers_text(self, fp, t_in, w_in, l_in):
        """
        print the text of the outliers when t == t_in, w == w_in, l == l_in
        """
        cluster_set = self.__xce.get_tailspin_cluster_set(t_in, w_in, l_in)
        title = 'OUTLIERS RESULTS for tailspin algorithm threshold = ' + t_in + ' window = ' + w_in + ' lookahead = ' + l_in + '\n'
        print >>fp, title
        clusters = cluster_set.get_clusters()
        for cluster in clusters:
            if len(cluster) == 1:
                for line_num in cluster:
                    print >>fp, str(self.__xrm.get_requirement_text_by_line(int(line_num))) + '\n'
    
    def print_wcc_outliers_text(self, fp, t_in):
        """
        print the text for the outliers when threshold_value = t_in 
        """
        cluster_set = self.__xce.get_wcc_cluster_set(t_in)
        title = "OUTLIERS RESULTS for wcc algorithm threshold = " + t_in + '\n'
        print >>fp, title
        outliers = cluster_set.get_outliers()
        for id in outliers:
            print >>fp, "ID " + str(self.__xrm.get_requirement_id_by_line(int(id))) + " " + str(self.__xrm.get_requirement_text_by_line(int(id))) + '\n'

    def print_clusters_size(self, consider_outliers):
        """
        Givena cluster experiment (i.e., a folder such as clusters-jaccard-lev-terms) this function inspects
        all the subfolders and count all the files in each folder. The number of files in each folder is the
        size of the cluster.
        @param consider_outliers: if False outliers are considered as the other clusters
                                  else outliers are not considered in the number of the clusters        
        """
        cluster_sets = self.__xce.get_cluster_sets()
        index = 1
        for c_set in cluster_sets:
            t = c_set.get_clusters_threshold()
            w = c_set.get_clusters_window()
            l = c_set.get_clusters_look_ahead()
            clusters = c_set.get_clusters()
            print index, 'CLUSTER NUMBER for tailspin algorithm threshold = ' + t + ' window = ' + w + ' lookahead = ' + l + '\n'
            index = index + 1

            if consider_outliers == False:
                c_num = len(clusters)
            else:
                outliers = 0
                for cluster in clusters:
                    if len(cluster) == 1:
                        outliers = outliers + 1
                c_num = len(clusters) - outliers

            print c_num

    def plot_clusters_size(self, consider_outliers):
        """
        Givena cluster experiment (i.e., a folder such as clusters-jaccard-lev-terms) this function inspects
        all the subfolders and count all the files in each folder. The number of files in each folder is the
        size of the cluster. The function plots these number.
        @param consider_outliers: if False outliers are considered as the other clusters
                                  else outliers are not considered in the number of the clusters        
        """
        cluster_sets = self.__xce.get_cluster_sets()
        cluster_num_list = list()

        for c_set in cluster_sets:
            clusters = c_set.get_clusters()

            if consider_outliers == False:
                c_num = len(clusters)
            else:
                outliers = 0
                for cluster in clusters:
                    if len(cluster) == 1:
                        outliers = outliers + 1
                c_num = len(clusters) - outliers


            cluster_num_list.append(c_num)

        pyplot.rcParams['font.size'] = 18
        pyplot.plot(cluster_num_list, 'b-')
    
        pyplot.xlabel('Experiment')
        pyplot.ylabel('Number of clusters')
        
        pyplot.show()
        pyplot.close()

    def plot_clusters_and_outliers_size(self):
        """
        This function plots the clusters size
        together with the part of clusters that are outliers
        """
        cluster_sets = self.__xce.get_cluster_sets()
        cluster_num_list = list()
        outlier_num_list = list()

        for c_set in cluster_sets:
            clusters = c_set.get_clusters()
            o_num = 0

            for cluster in clusters:
                if len(cluster) == 1:
                    o_num = o_num + 1
                    
            c_num = len(clusters)


            cluster_num_list.append(c_num)
            outlier_num_list.append(o_num)

        pyplot.rcParams['font.size'] = 18
        pyplot.plot(cluster_num_list, 'b-', label = "Number of Clusters")
        pyplot.plot(outlier_num_list, 'r--', label = "Number of Outliers")
    
        pyplot.xlabel('Experiment')

        pyplot.legend(loc = 2)
                
        pyplot.show()
        pyplot.close()


    def __compute_average_cluster_len(self, clusters):
        """
        Compute the average len for the cluster set
        @param clusters: list of clusters
        @return average number of requirements per cluster
        """

        return numpy.mean([len(c) for c in clusters])

    def __compute_stddev(self, clusters):
        """
        Compute the standard deviation of the number of elements
        for each cluster
        @param clusters: list of clusters
        @return standard deviation of the number of requirements per cluster
        """

        return numpy.std([len(c) for c in clusters])
        
    
    def get_best_cluster(self):
        """
        This function returns the clustering set which is more similar
        to the document in terms of number of sections, average section len
        and standard deviation
        """

        section_number = 14 #this is hard coded since the number of sections for EIRENE is 14, because the introduction is not considered
        TOLERANCE = 5       
        cluster_sets = self.__xce.get_cluster_sets()
        for c_set in cluster_sets:
            clusters = c_set.get_clusters()
            if len(clusters) > section_number - TOLERANCE and \
            len(clusters) < section_number + TOLERANCE:
                print c_set.get_clusters_dir()
                print "cluster len = ", len(clusters)
                avg = self.__compute_average_cluster_len(clusters)
                stddev = self.__compute_stddev(clusters)
                print "average = ", avg
                print "stddev = ", stddev

CLUSTER_PATH = './2007-eirene-tailspin/'

x = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')

directory = 'clusters-jaccard-lev-terms'
e = XMLClusterExperiment(CLUSTER_PATH + directory,'','tailspin', 583, 'jaccard_lev_terms')
a = XMLReqAnalyzer(x,e)

a.get_best_cluster()

