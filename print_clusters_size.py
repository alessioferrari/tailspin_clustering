from XMLReqAnalyzer import XMLReqAnalyzer
from XMLReqManager import XMLReqManager
from XMLClusterExperiment import XMLClusterExperiment

CLUSTER_PATH = './2007-eirene-tailspin/'

x = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')

directory = 'clusters-lev-terms'
e = XMLClusterExperiment(CLUSTER_PATH + directory,'','tailspin', 583, 'lev_terms')
a = XMLReqAnalyzer(x,e)

a.print_clusters_size(False)
