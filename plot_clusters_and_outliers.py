from XMLReqAnalyzer import XMLReqAnalyzer
from XMLReqManager import XMLReqManager
from XMLClusterExperiment import XMLClusterExperiment

CLUSTER_PATH = './2007-eirene-tailspin/'       
DIRECTORY = 'clusters-jaccard-lev-terms'

x = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')
e = XMLClusterExperiment(CLUSTER_PATH + DIRECTORY,'','tailspin', 583, 'jaccard_terms')
a = XMLReqAnalyzer(x,e)

a.plot_clusters_and_outliers_size()
