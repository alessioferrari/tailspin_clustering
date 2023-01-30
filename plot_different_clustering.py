from XMLReqAnalyzer import XMLReqAnalyzer
from XMLReqManager import XMLReqManager
from XMLClusterExperiment import XMLClusterExperiment
import matplotlib
import numpy
from matplotlib import pyplot


"""
This program plots the comparison among the cluster sizes
of jaccard, levenstein and combination of them
"""

def __get_cluster_sizes(cluster_sets, consider_outliers):

        cluster_sizes = list()
        
        for c_set in cluster_sets:
            clusters = c_set.get_clusters()

            if consider_outliers == False:
                c_num = len(clusters)
                o_num = 0
            else:
                o_num = 0
                for cluster in clusters:
                    if len(cluster) == 1:
                        o_num = o_num + 1
                c_num = len(clusters) - o_num

            cluster_sizes.append(c_num)

        return cluster_sizes

def plot_different_clustering_sizes(path, consider_outliers):
    """
    This function plots the cluster sizes for all the experiments in a folder
    """
    
    e_jaccard = XMLClusterExperiment(path + 'clusters-jaccard-terms','','tailspin', 583, 'jaccard_terms')
    e_lev = XMLClusterExperiment(path + 'clusters-lev-terms','','tailspin', 583, 'lev_terms')
    e_jac_lev = XMLClusterExperiment(path + 'clusters-jaccard-lev-terms','','tailspin', 583, 'jac_lev_terms')

    c_jaccard = e_jaccard.get_cluster_sets()
    c_lev= e_lev.get_cluster_sets()
    c_jac_lev = e_jac_lev = e_jac_lev.get_cluster_sets()

    c_sizes_jac = __get_cluster_sizes(c_jaccard, consider_outliers)
    c_sizes_lev = __get_cluster_sizes(c_lev, consider_outliers)
    c_sizes_jac_lev = __get_cluster_sizes(c_jac_lev, consider_outliers)

    pyplot.rcParams['font.size'] = 12
    pyplot.rcParams['font.family'] = 'serif'
    
    pyplot.axhline(y=145, xmin=0, xmax=.33, c='k', ls='--')
    #pyplot.axvline(x=22, ymin=0, ymax=.32, c='k', ls='--')
    pyplot.text(x=-4, y=145, s='145')

    pyplot.axhline(y=28, xmin=0, xmax =.157, c='k', ls='--')
    pyplot.text(x=-3, y=28, s='28')

    pyplot.plot(c_sizes_jac, 'b--', label = "$\sigma_{jac}$")
    pyplot.plot(c_sizes_lev, 'r-', label = "$\sigma_{lev}$")
    pyplot.plot(c_sizes_jac_lev, 'g-.', label = "$\sigma_{jac-lev}$")

    pyplot.xlabel('Hidden Structure Candidate')
    pyplot.ylabel('Number of Clusters')

    #vertical lines
    pyplot.axvline(x=6, ymin=0, ymax=1, c = 'k')
    pyplot.axvline(x=12, ymin=0, ymax=1, c = 'k')
    pyplot.axvline(x=18, ymin=0, ymax=1, c = 'k')
    pyplot.axvline(x=24, ymin=0, ymax=1, c = 'k')

    pyplot.annotate('$\\tau = 0$', xy=(1,530), fontsize = 11)
    pyplot.annotate('$\\tau = 0.1$', xy=(6.5,530), fontsize = 11)
    pyplot.annotate('$\\tau = 0.2$', xy=(12.5,530), fontsize = 11)
    pyplot.annotate('$\\tau = 0.3$', xy=(18.5,530), fontsize = 11)


    pyplot.legend(loc = 4)
            
    pyplot.show()
    pyplot.close()


plot_different_clustering_sizes('2007-eirene-tailspin/', False)
