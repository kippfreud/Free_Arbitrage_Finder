'''
Classes for holding tag webpage elements.

SpiceBucks
'''

#------------------------------------------------------------------

from bs4.element import Tag

import util.utilities as ut
from util.message import message

#------------------------------------------------------------------

class CTag():
    '''
    Wrapper for a soup tag.
    '''
    def __init__(self, souptag):
        '''
        Instantiates class.
        '''
        if not isinstance(souptag, Tag):
            message.logError("Given souptag is not a bs4.element.Tag instance.",
                             "CTag::__init__")
            ut.exit(0)
        
        self.m_tag = souptag
        name = souptag.getText()
        if name != None:
            self.m_name = name
        else:
            self.m_name = "tag_name"
            
    def __repr__(self):
        '''
        Defines what to print when print() is called on this class.
        '''
        return "Tag: " + self.m_name
        
    #------------------------------------------------------------------
    # public methods
    #------------------------------------------------------------------
    
    def getAttr(self, attr_name):
        '''
        Will return the attribute with attribute name equal to the string :param:`attr_name, or a NoneType instance
        if not such attributes exist.
        
        :param attr_name: A string attribute name to look for.
        '''
        if not isinstance(attr_name, str):
            message.logError("Given attribute name must be a string instance.",
                             "CTag::getAttr")
            ut.exit(0)
        if not self.m_tag.has_attr(attr_name): return None
        return self.m_tag.attrs[attr_name]
    
    def getChildren(self):
        '''
        Returns all the children of this class as CTag instances.
        '''
        ret = list(self.m_tag.children)
        return [ CTag(r) for r in ret ]
    
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
            ret = self.m_tag.findAll(True, {"class":class_names})
        elif isinstance(class_names, str):
            ret = self.m_tag.findAll(True, {"class":[class_names]})
        else:
            message.logError("Given paramer class_names must be a list containing only string instances, " +
                             "or must be a string instance.")
            ut.exit(0)
        return [CTag(tag) for tag in ret]
    
    def getClassName(self):
        """
        Returns name of this tags class.
        """
        return self.m_tag.attrs["class"]
    
    def getName(self): 
        '''
        returns self.m_name parameter.
        '''
        return self.m_name
    
    def getRaw(self):
        '''
        Returns the raw string html tag.
        '''
        return str(self.m_tag)
    
    def hasAttr(self, attr_name):
        '''
        Will return True if any attributes of this tag have name equal to the given :param:`attr_name`.
        False otherwise.
        '''
        return self.m_tag.has_attr(attr_name)
