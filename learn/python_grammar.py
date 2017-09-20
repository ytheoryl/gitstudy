#!/usr/bin/env python

import os
import sys
import commands
import traceback
import abc
import six
import thread
import threading
from abc import ABCMeta, abstractmethod

def swap_two_variable(a, b):
    """ swap two values
    refer: http://wuzhiwei.net/be_pythonic/
    """
    a, b = b, a
    return a, b

def ternary_operator(condition, value1, value2):
    """ the ternary operator: condition ? value1 : value2
        condition = true, return value1
        condition = false, return value2
    """
    return value1 if condition else value2


def open_file_write(dir, file, data):
    """ replace "try ... except ... finally ..." to ensure file will be closed whatever
    refer: http://yuez.me/python-zhong-de-guan-jian-zi-with-xiang-jie/
    """
    if not os.path.exists(dir):
        raise Exception('dir(%s) not existed' % dir)
    full_path = os.path.join(dir, file)
    with open(full_path, "w") as file:
        file.write(data)
        
def reverse_string(str):
    """ reverse string
        eg "abcd" => "dcba"
    """
    return str[::-1]
  
def list_deduce(li, expression):
    """ list deduce
        eg, li = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] => list_deduce(li, lambda x : x % 2) = > [1, 3, 5, 7]
    """
    return [x for x in li if expression(x)]  
     
def dict_default_value(dic, key, default):
    """dict: get(key,default) to get value by key. if key not existed, set dict[key] = default
    """
    return dic.get(key, default)

def for_else_grammar(li, expression):
    """ for...else... grammar
    """
    for x in li:
        if expression(x):
            return x
    else:
        return None
    
def enumerate_index_value(li):
    """ once get index and value from list
    refer: http://wuzhiwei.net/be_pythonic/
    """
    for i, e in enumerate(li, 0):
        print i, e
    
def create_key_value_pair(key, value):
    """ create key value pair by zip
    eg, keys = ['Name', 'Sex', 'Age']
        values = ['Tim', 'Male', 23]
        dict(zip(keys, values)) => #{'Age': 23, 'Name': 'Tim', 'Sex': 'Male'}
    """
    return dict(zip(keys, values))

def function_parameter(*args, **kwargs):
    """ function multi parameter
        a = 1,2,3,4
        b = {"aa":"aa", "bb":"bb"}
        function_parameter(a, b)
        (1, 2, 3, 4)
        {'aa': 'aa', 'bb': 'bb'}
    """
    for arg in args:
        print arg
        
    for keyword, value in kwargs:
        print keyword, value
        
def const_define():
    import const
    const.NAME = 'IBM'
    const.EMAIL = 'ibm.com'
    
    const.EMAIL = 'a'


""" decorator
foo()

hello, foo
i am foo
goodby, foo
"""
def hello(fn):
    def wrapper():
        print "hello, %s" % fn.__name__
        fn()
        print "goodby, %s" % fn.__name__
    return wrapper
 
@hello
def foo():
    print "i am foo"
############################################################################################################
""" call stack: when exception happened, print call stack
"""
def exception_traceback():
    try:
        pass
    except Exception, e:
        print traceback.format_exc()
############################################################################################################
""" invoke shell command
"""
def invoke_shell(cmd):
    ret = commands.getstatusoutput(cmd)
    if ret[0]:
        raise Exception("status: %s; output: %s" % (ret[0], ret[1]))
    return ret
############################################################################################################
""" Six provides simple utilities for wrapping over differences between Python 2 and Python 3
"""
def dispatch_types(value):
    if isinstance(value, six.integer_types):
        print "integer_types"
    elif isinstance(value, six.class_types):
        print "class_types"
    elif isinstance(value, six.string_types):
        print "string_types"
############################################################################################################
""" python build in function
"""
class Buildin(object):
    class FunctionObject(object):
        def __init__(self, greeting):
            self.__greeting = greeting
        
        """ function object
            eg, Buildin.get_build_in_call()
        """
        def __call__(self):
            print "self.__greeting = %s" % self.__greeting
    
    @staticmethod
    def get_build_in_call():
        return Buildin.FunctionObject("hello, function object")()
    
############################################################################################################
""" python closure design
"""
class Test(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def add(self):
        return lambda : self.a + self.b
    
    def set_a(self, a):
        self.a = a
        
    def set_b(self, b):
        self.b = b

'''
def main(argv=None):
    try:
        test = Test(1, 1)
        add = test.add()
        print add()
        
        test.set_a(3)
        print add()
         
    except Exception, e:
        print "traceback: %s" % traceback.format_exc()
 
if __name__ == "__main__":
    
    sys.exit(main())
    
output:
2
4
'''

""" define abstract class by abc module
"""
class IInterface(object):
    """ define abstract base class
    refer: http://www.cnblogs.com/wupeiqi/p/4766801.html
    """
    
    """ static field
    """
    class_property = "class property"
    
    def __init__(self):
        self.__name = None
    
    @property
    def name(self):
        """
        invoke method: instance.get_name
        """
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value
        
    @name.deleter
    def name(self):
        self.__name = None
    
    @abstractmethod
    def abstract_method(self):
        raise NotImplementedError('get_metric_names')

    @staticmethod
    def static_method():
        print "static_method"
        
    @classmethod
    def class_method(cls):
        print cls.class_property
        
    def common_method(self):
        self.abstract_method()

############################################################################################################
""" singleton design pattern
"""
class Singleton(object):
    __instance = None
    __lock = threading.Lock()
    def __new__(cls):
        if cls.__instance is None:
            with Singleton.__lock:
                if cls.__instance is None:
                    cls.__instance = cls()
        return cls.__instance
    
    @staticmethod
    def instance():
        return Singleton.__instance if Singleton.__instance else Singleton()
############################################################################################################


def main(argv=None):
    try:
        
        print __name__
        
    except Exception, e:
        print traceback.format_exc()


if __name__ == '__main__':
    sys.exit(main())
   








    