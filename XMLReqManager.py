from nltk.stem.porter import PorterStemmer
from xml.dom.minidom import *
import nltk
import sys
import xml.dom.minidom
import numpy

REQ_TAG = 'req'
ID_TAG = 'id'
BODY_TAG = 'text_body'
PARAGRAPH_TAG = 'p'

class XMLReqManager:
    """
    This class allows managing requirements in XML format
    """
    
    def __init__(self, dtd_file_name, req_file_name):
        self.__dtd_file_name = dtd_file_name
        self.__req_file_name = req_file_name
        self.__stopwords = nltk.corpus.stopwords.words('english')
        self.__commonwords = []
        self.__reqs = []
        self.__pars = []
        
    def __get_text(self, node, current_text):
        if node.nodeType == Node.TEXT_NODE and \
            not node.parentNode._get_tagName() == 'modifier' and \
            not node.parentNode._get_tagName() == 'crossref' and \
            not node.data.isspace() and \
            not node.data == None:
            current_text.append(node.data)
        else:
            for sub_node in node.childNodes:
                self.__get_text(sub_node, current_text)

    def get_requirements(self):
        """
        This method returns a possibly empty textual requirements list, 
        where each item is a couple [ID, req], where req is a list that might 
        contain more than one element if the requirement is made of more than 
        one sentence
        @return: 
            The list of requirements, if the file exists
            None, otherwise
            
        """
        try:
            if len(self.__reqs) == 0:
                doc = xml.dom.minidom.parse(self.__req_file_name)
                reqs = doc.getElementsByTagName(REQ_TAG)
                reqs_text = list()
                for req in reqs:
                    req_id = req.getAttribute(ID_TAG)
                    text = list()
                    self.__get_text(req, text)
                    req_item = [req_id, text]
                    reqs_text.append(req_item)
                self.__reqs = reqs_text
            
            return self.__reqs
        except IOError: 
            print "Cannot open requirements file: ", self.__req_file_name
        except:
            print "Unexpected error: ", sys.exc_info()[0]
            raise

    def get_paragraphs(self):
        """
        This function returns the paragraphs number in the requirements
        document
        @return: 
            The list of paragraphs, if the file exists
            None, otherwise
        """
        try:
            if len(self.__pars) == 0:
                doc = xml.dom.minidom.parse(self.__req_file_name)
                pars = doc.getElementsByTagName(PARAGRAPH_TAG)
                for par in pars:
                    par_id = par.getAttribute(ID_TAG)
                    self.__pars.append(par_id)
            return self.__pars
        except IOError: 
            print "Cannot open requirements file: ", self.__req_file_name
        except:
            print "Unexpected error: ", sys.exc_info()[0]
            raise

    def get_number_of_sections(self):
        """
        This function returns the total number of LEVEL 1 sections
        (i.e., those that do not contain dots in the id)
        """
        sections_number = 0
        if len(self.__pars) == 0:
            self.get_paragraphs()
        
        for par_id in self.__pars:
            if par_id.find('.') == -1 and par_id != "":
                sections_number = sections_number + 1        
        return sections_number 

    def get_standard_dev_number_of_req_per_section(self):
        """
        returns the standard deviation of number of requirements for each section
        """
        num_req_list = list()
        try:
            doc = xml.dom.minidom.parse(self.__req_file_name)
            pars = doc.getElementsByTagName(PARAGRAPH_TAG)
            for par in pars:
                par_id = par.getAttribute(ID_TAG)
                if par_id.find('.') == -1 and par_id != "":
                    reqs = par.getElementsByTagName(REQ_TAG)
                    if len(reqs) != 0: #WARNING: some sections have no requirements in EIRENE
                        num_req_list.append(len(reqs))

            print num_req_list
            return numpy.std(num_req_list)
                    
        except IOError: 
            print "Cannot open requirements file: ", self.__req_file_name
        except:
            print "Unexpected error: ", sys.exc_info()[0]
            raise
    
    def get_requirements_text(self):
        """
        This function returns a lists where each element of the list is the 
        entire text of a requirement 
        """
        reqs = self.get_requirements()
        req_text = [' '.join(line for line in req) for id, req in reqs]
        return req_text
    
    def get_requirements_ids(self):
        """
        This function returns a list containing all the id of the requirements 
        @attention: this list might contain duplicates, indeed some requirements
        might have been split into sub-requirements keeping the same id
        """
        reqs = self.get_requirements()
        reqs_id = [id for id, req in reqs]
        return reqs_id
    
    def get_line_id_map(self):
        """
        This function returns a list of couples (line number, id)
        where each line of the output file is associated with the
        id of the requirement
        """
        ids = self.get_requirements_ids()
        couples = [[i+1,id] for i, id in enumerate(ids)]
        return couples
    
    def get_requirement_id_by_line(self, line_num):
        """
        Given the line number of the produced output file this
        function returns the requirement id associated to the line
        """
        id_map = self.get_line_id_map()
        for line, id in id_map:
            if line == line_num:
                return id
            
        return None
    

    def get_requirement_text_by_id(self, r_id):
        reqs = self.get_requirements()
        req  = [r for id, r in reqs if id == r_id]
        req_str = ''.join(s for string in req for s in string)
        return req_str.lstrip()
        
    def get_requirement_text_by_line(self, line_num):
        reqs = self.get_requirements()
        req  = [r for id, r in reqs if id == self.get_requirement_id_by_line(line_num)]
        req_str = ''.join(s for string in req for s in string)
        return req_str.lstrip()

    def create_requirements_file(self, file_output_name, mode):
        """
        Create a textual file for the requirements to be processed by the algorithm.
        Each line of the file corresponds to a requirement. The option mode allows
        to choose if one wants to save only the content (i.e., stemmed terms of the
        requirements separated by ':'), only the pos (i.e., pos tags separated by ':'),
        or both (two lists, one for stemmed terms and one for pos, separated by a tab)
        @param file_output_name: textual name of the file where the requirements shall be saved
        @param mode: 'content', 'pos' or 'content_pos', if one wants to save the content,
        the pos or both 
        """
        try:
            output_f = open(file_output_name, 'w')
        except IOError:
            print "Cannot open requirements file: ", self.file_output_name
            return None
        
        requirements_list = self.get_requirements_text()
        
        clean_req_list = list()
        for req in requirements_list:
            clean_req = list()
        
            word_req_list = nltk.word_tokenize(req) 
            postagged_words = nltk.pos_tag(word_req_list)
            
            for (word, tag) in postagged_words:
                if word.lower() not in self.__stopwords and\
                word.lower().isalpha() and\
                word.lower() not in self.__commonwords:
                    stemmed_w = PorterStemmer().stem_word(word)
                    tagged_stemmed_w = (stemmed_w, tag)
                    clean_req.append(tagged_stemmed_w)
            clean_req_list.append(clean_req)
    
        for req in clean_req_list:
        #write the stemmed words    
            if mode == 'content' or mode == 'content_pos':    
                for (word, tag) in req:
                    output_f.writelines(word.lower())
                    if req.index((word, tag)) != (len(req)-1):
                            output_f.write(':')
        #write the pos
            if mode == 'content_pos':
                output_f.write('        ')
            
            if mode == 'pos' or mode == 'content_pos':
                for (word, tag) in req:
                        output_f.writelines(tag)
                        if req.index((word, tag)) != (len(req)-1):
                                output_f.write(':')
            output_f.write('\n')
        
        output_f.close()


        
    
#x = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')
#print x.get_standard_dev_number_of_req_per_section()

#t = x.create_requirements_file('2007 eirene fun 7 - INPUT.txt', 'content_pos')
#print x.get_line_id_map()
#strings = x.get_requirement_text_by_line(205)
#print ''.join(s for string in strings for s in string).lstrip()


