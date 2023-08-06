from ctypes import *
import os

if os.name == 'nt':
    dllpath = os.path.dirname(os.path.abspath(__file__)) + "/SuffixTreePyBinding.dll"
    #dllpath = os.path.dirname(os.path.abspath(__file__)) + "/../../x64/Release/SuffixTreePyBinding.dll"
else:
    dllpath = os.path.dirname(os.path.abspath(__file__)) + "/libSuffixTreePyBinding.so"

class SuffixQueryTree(object):
    CHAR_ANY = ord('.')
    CHAR_WORD = ord('w')
    CHAR_STRING_START = ord('^')
    CHAR_STRING_END = ord('$')

    def __init__(self, preserveString:bool, strs:list = None):
        
        lib = cdll.LoadLibrary(dllpath)
        pylib = pydll.LoadLibrary(dllpath)

        lib.createSuffixQueryTreePy.argtypes = [ py_object,c_bool ] # list string, persist, budgetRatio, sampleRate
        lib.createSuffixQueryTreePy.restype = py_object # pointer

        lib.createSuffixQueryTreePyWithCache.argtypes = [ py_object,c_bool,c_double,c_double ] # list string, persist, budgetRatio, sampleRate
        lib.createSuffixQueryTreePyWithCache.restype = py_object # pointer

        lib.findStringIdx_qtreePy.argtypes = [ py_object,py_object,c_bool ] # tree_capsule, string
        lib.findStringIdx_qtreePy.restype = py_object # list int

        pylib.findString_qtreePy.argtypes = [ py_object, py_object,c_bool ] # tree_capsule, string
        pylib.findString_qtreePy.restype = py_object # list string

        lib.cacheIntermediateNodePy.argtypes = [ py_object, c_double, c_double ] # tree_capsule, budgetRatio, sampleRate
        lib.cacheIntermediateNodePy.restype = py_object # list string

        pylib.findString_QTree_wildcardPy.argtypes = [ py_object, py_object,c_bool ] # tree_capsule, list_charset
        pylib.findString_QTree_wildcardPy.restype = py_object # list string

        lib.findStringIdx_QTree_wildcardPy.argtypes = [ py_object, py_object,c_bool ] # tree_capsule, list_charset
        lib.findStringIdx_QTree_wildcardPy.restype = py_object # list int

        lib.allString_SuffixQueryTreePy.argtypes = [ py_object ] # tree_capsule
        lib.allString_SuffixQueryTreePy.restype = py_object # list string

        lib.strNum_SuffixQueryTreePy.argtypes = [ py_object ] # tree_capsule
        lib.strNum_SuffixQueryTreePy.restype = c_int32 # list string

        #----------------------- serialize and deserialize ----------------

        lib.saveSuffixQueryTreeToFilePy.argtypes = [ py_object, c_char_p ]  # tree_capsule, path

        lib.saveSuffixQueryTreePy.argtypes = [ py_object ] # tree_capsule, path
        lib.saveSuffixQueryTreePy.restype = py_object # bytes

        lib.readSuffixQueryTreeFromFilePy.argtypes = [ c_char_p ]  # path
        lib.readSuffixQueryTreeFromFilePy.restype = py_object #tree_capsule

        lib.readSuffixQueryTreePy.argtypes = [ py_object ]  # bytes
        lib.readSuffixQueryTreePy.restype = py_object #tree_capsule

        self.lib = lib
        self.pylib = pylib
        self.preserveString = preserveString
        self.c_qtree = None
        if strs is not None:
            self.initStrings(strs)

    def serialize(self,path = None):
        if path is None:
            return self.lib.saveSuffixQueryTreePy(self.c_qtree)
        else:
            path = path.encode('utf-8')
            self.lib.saveSuffixQueryTreeToFilePy(self.c_qtree, path)

    def zippedSerialize(self,path):
        import zlib
        b1 = self.lib.saveSuffixQueryTreePy(self.c_qtree)
        b1 = zlib.compress(b1,3)
        with open(path,"wb") as f:
            f.write(b1)

    def zippedDeserialize(self,path):
        import zlib
        with open(path,"rb") as f:
            b1 = f.read()
        b1 = zlib.decompress(b1)
        self.c_qtree = self.lib.readSuffixQueryTreePy(b1)
        #TODO modify python side preserveString

    def deserialize(self,content = None):
        if type(content) == bytes:
            self.c_qtree = self.lib.readSuffixQueryTreePy(content)
        elif type(content) == str:
            content = content.encode('utf-8')
            self.c_qtree = self.lib.readSuffixQueryTreeFromFilePy(content)
        else:
            raise Exception("content has to be either a string or bytes")
        #TODO modify python side preserveString


    def findStringIdx(self,s:str,case_sensitive:bool = True): 
        return self.lib.findStringIdx_qtreePy(self.c_qtree,s,case_sensitive)

    def findString(self,s:str,case_sensitive:bool = True): 
        return self.pylib.findString_qtreePy(self.c_qtree,s,case_sensitive)

    def initStrings(self,strs:list):
        self.numStr = len(strs)
        self.c_qtree = self.lib.createSuffixQueryTreePy(strs,self.preserveString)

    def initStringsWithCache(self,strs:list):
        self.numStr = len(strs)
        self.c_qtree = self.lib.createSuffixQueryTreePyWithCache(strs,self.preserveString,1.5,0.01)

    def findStringIdx_wildCard(self,s:list,case_sensitive:bool = True): 
        return self.lib.findStringIdx_QTree_wildcardPy(self.c_qtree,s,case_sensitive)

    def findString_wildCard(self,s:list,case_sensitive:bool = True): 
        return self.pylib.findString_QTree_wildcardPy(self.c_qtree,s,case_sensitive)

    def cacheNodes(self,budgetRatio:float = 0.5,sampleRate:float = 0.01):
        log = self.lib.cacheIntermediateNodePy(self.c_qtree,budgetRatio,sampleRate)
        return log

    def getStrings(self):
        return self.lib.allString_SuffixQueryTreePy(self.c_qtree)

    def getStrNum(self):
        return self.lib.strNum_SuffixQueryTreePy(self.c_qtree)

class SuffixTree(object):
    """description of class"""

    def __init__(self, preserveString:bool, strs:list = None):
        lib = cdll.LoadLibrary(dllpath)
        pylib = pydll.LoadLibrary(dllpath)

        lib.createSuffixTreePy.argtypes = [ py_object,c_bool ] # list string, persist
        lib.createSuffixTreePy.restype = py_object # capsule

        lib.findStringIdxPy.argtypes = [ py_object,py_object ] # tree_capsule, string
        lib.findStringIdxPy.restype = py_object # list int

        pylib.findStringPy.argtypes = [ py_object,py_object ] # tree_capsule, string
        pylib.findStringPy.restype = py_object # list string

        lib.SuffixTree_toQueryTree.argtypes = [ py_object ] # tree_capsule, string
        lib.SuffixTree_toQueryTree.restype = py_object # list string

        lib.suffixTreeAddStringsPy.argtypes = [ py_object, py_object ] # tree_capsule, list string

        lib.suffixTreeAddStringPy.argtypes = [ py_object, py_object ] # tree_capsule, string

        lib.allString_SuffixTreePy.argtypes = [ py_object ] # tree_capsule
        lib.allString_SuffixTreePy.restype = py_object # list string

        lib.strNum_SuffixTreePy.argtypes = [ py_object ] # tree_capsule
        lib.strNum_SuffixTreePy.restype = c_int32 # list string


        self.lib = lib
        self.pylib = pylib
        self.preserveString = preserveString
        self.c_tree = None
        if strs is not None:
            self.addStrings(strs)

    def getStrings(self):
        return  self.lib.allString_SuffixTreePy(self.c_tree)

    def createQueryTree(self):
        q = SuffixQueryTree(self.preserveString)
        q.c_qtree = self.lib.SuffixTree_toQueryTree(self.c_tree)
        return q;

    def addStrings(self, strs:list):
        if self.c_tree is None:
            self.c_tree = self.lib.createSuffixTreePy( strs,self.preserveString)
        else:
            self.lib.suffixTreeAddStringsPy(self.c_tree,strs)

    def addString(self,s:str):
        if self.c_tree is None:
            self.c_tree = self.lib.createSuffixTreePy( [s],self.preserveString)
        else:
            self.lib.suffixTreeAddStringPy(self.c_tree,s)

    def findStringIdx(self,s:str):
        return self.lib.findStringIdxPy(self.c_tree,s)

    def findString(self,s:str):
        return self.pylib.findStringPy(self.c_tree,s)

    def getStrNum(self):
        return self.lib.strNum_SuffixTreePy(self.c_tree)
