from XMLReqAnalyzer import XMLReqAnalyzer
from XMLReqManager import XMLReqManager
from XMLClusterExperiment import XMLClusterExperiment

def get_best_cluster():
    """
    This function returns the clustering set which is more similar
    to the document in terms of number of sections, average section len
    and standard deviation
    """
    CLUSTER_PATH = './2007-eirene-tailspin/'

    x = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')

    directory = 'clusters-jaccard-terms'
    e = XMLClusterExperiment(CLUSTER_PATH + directory,'','tailspin', 583, 'jaccard_terms')
    a = XMLReqAnalyzer(x,e)

    a.get_best_cluster()

get_best_cluster()
