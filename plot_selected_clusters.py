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
    

    e_lev = XMLClusterExperiment(path + 'clusters-lev-terms','','tailspin', 583, 'lev_terms')
    e_jac_lev = XMLClusterExperiment(path + 'clusters-jaccard-lev-terms','','tailspin', 583, 'jac_lev_terms')

    c_lev= e_lev.get_cluster_sets()
    c_jac_lev = e_jac_lev.get_cluster_sets()

    c_sizes_lev = __get_cluster_sizes(c_lev, consider_outliers)
    c_sizes_jac_lev = __get_cluster_sizes(c_jac_lev, consider_outliers)
    
    pyplot.rcParams['font.size'] = 12
    pyplot.rcParams['font.family'] = 'serif'

    #lines for the best candidate
    pyplot.axhline(y=14, xmin=0, xmax=.39, c='k', ls='--')
    pyplot.axvline(x=7, ymin=0, ymax=.2, c='k', ls='--')
    pyplot.text(x=-0.6, y=13, s='14')

    pyplot.annotate("Best Hidden \n Structure", xy=(7, 14), xycoords='data',
                xytext=(10, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle="->")
                )

    
    pyplot.plot(c_sizes_lev, 'r-', label = "$\sigma_{lev}$")
    pyplot.plot(c_sizes_jac_lev, 'g-.', label = "$\sigma_{jac-lev}$")

    pyplot.xlabel('Hidden Structure Candidate')
    pyplot.ylabel('Number of Clusters')

    pyplot.xlim(xmax=18)
    pyplot.ylim(ymax=75)

    pyplot.axvline(x=6, ymin=0, ymax=1, c = 'k')
    pyplot.axvline(x=12, ymin=0, ymax=1, c = 'k')
    #pyplot.axvline(x=17, ymin=0, ymax=1, c = 'k')



    pyplot.annotate('$\\tau = 0$', xy=(2,40), fontsize = 12)
    pyplot.annotate('$\\tau = 0.1$', xy=(8,40), fontsize = 12)
    pyplot.annotate('$\\tau = 0.2$', xy=(14,40), fontsize = 12)

    pyplot.legend(loc = 2)

         
    pyplot.show()
    pyplot.close()


plot_different_clustering_sizes('selected_experiments_eirene/', False)
