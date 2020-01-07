'''
Classes for holding webpages.

SpiceBucks
'''

#------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

import util.utilities as ut
from util.message import message
from webscraping.tag import CTag

#------------------------------------------------------------------

DEFAULT_HEADERS = {'User-Agent':'Mozilla/5.0'}
DEFAULT_LINK_ATTR_NAME = "href"

#------------------------------------------------------------------

class CWebsite():
    '''
    A class representing a website.
    '''
    def __init__(self, url, home_url, headers=DEFAULT_HEADERS, name="Website"):
        '''
        Instantiates class.
        '''
        if not isinstance(url, str):
            message.logError("Given URL is not a string instance.",
                             "CWebsite::__init__")
            ut.exit(0)
        if not isinstance(home_url, str):
            message.logError("Given home URL is not a string instance.",
                             "CWebsite::__init__")
            ut.exit(0)
            
        response = requests.get(url, headers=headers)
        
        self.m_url = url
        self.m_home_url = home_url
        self.m_headers = headers
        self.m_websoup = BeautifulSoup(response.text, "html.parser")
        self.m_name = name
        
    #------------------------------------------------------------------
    # public methods
    #------------------------------------------------------------------
    
    def getAttrs(self, class_names, link_attr_name):
        '''
        Will return a list of attributes contained in elements with class name equal to one of the string names in 
        :param:`class_names`, these attributes of these elements must have attribute name given by :param:`link_attr_name`.
        '''            
        tags = self.getClasses(class_names)
        ret = []
        for t in tags:
            if t.hasAttr(link_attr_name):
                ret.append(t.getAttr(link_attr_name))
        return ret
    
    def getClasses(self, class_names):
        '''
        Will return a list of tags with class name equal to one of the names in the list of :param:`class_names`,
        or is equal to the string :param:`class_names` if :param:`class_names` is a string.
        
        :param class_names: A list of string class names to look for, or a string class name to look for.
        '''
        if isinstance(class_names, list):
            for class_name in class_names:
                if not isinstance(class_name, str):
                    message.logError("Given paramer class_names must be a list containing only string instances, " +
                                     "or must be a string instance.")
                    ut.exit(0)
            ret = self.m_websoup.findAll(True, {"class":class_names})
        elif isinstance(class_names, str):
            ret = self.m_websoup.findAll(True, {"class":[class_names]})
        else:
            message.logError("Given paramer class_names must be a list containing only string instances, " +
                             "or must be a string instance.")
            ut.exit(0)
        return [CTag(tag) for tag in ret]
    
    def getName(self):
        '''
        returns website name.
        '''
        return self.m_name
    
    def getURL(self):
        '''
        returns website URL.
        '''
        return self.m_url
    
    def getHomeURL(self):
        '''
        returns URL of home page.
        '''
        return self.m_home_url