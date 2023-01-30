"""
Created on 05/lug/2011

@author: alessio
"""
from XMLReqAnalyzer import XMLReqAnalyzer
from XMLReqManager import XMLReqManager
from XMLClusterExperiment import XMLClusterExperiment
import os
import errno

CLUSTER_PATH = './2007-eirene-tailspin/'   
RESULT_PATH = './tailspin-clusters-results/'      

x = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')


directory = 'clusters-jaccard-lev-terms'
e = XMLClusterExperiment(CLUSTER_PATH + directory,'','tailspin', 583, 'jaccard_lev_terms')
a = XMLReqAnalyzer(x,e)

path = RESULT_PATH + directory + '/'
try:
    os.makedirs(path)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
    
a.print_single_tailspin_cluster_experiment(path, '01', '2', '1')
    
print 'done'   
