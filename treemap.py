#!/usr/bin/env python
"""
    Author: Omar Avelar
    
    DESCRIPTION
    ===========
    Simple class extension of a dictionary data type that can print in a tree
    esque way to see what you got organized in it, also tested in Python 2.6.
    
    EXAMPLE
    =======
    >>> a = { 'cat':{'legs' : 4, 'heads' : 1}, 'dog':{'legs' : 4, 'heads' : 1} }
    >>> b = TreeMap(a)
    >>> b.tree()

    +--[ dog ]
    |     \_.--[ legs = 4 ]
    |     \_.--[ heads = 1 ]
    +--[ cat ]
    |     \_.--[ legs = 4 ]
    |     \_.--[ heads = 1 ]


    >>> d = { 'A':{'a':1, 'b':2, 'c':{'d':0, 'e':1}}, 'W':{'x':99, 'y':100} }
    >>> e = TreeMap(d)
    >>> e.tree()

    +--[ A ]
    |     \_.--[ a = 1 ]
    |     +--[ c ]
    |     |     \_.--[ e = 1 ]
    |     |     \_.--[ d = 0 ]
    |     \_.--[ b = 2 ]
    +--[ W ]
    |     \_.--[ y = 100 ]
    |     \_.--[ x = 99 ]

"""
import string

class TreeMap(dict):
    """
    Extension of the dictionary class that has tree printing,
    It figures out common stuff and organizes while printing.
    """
    def tree(self, depth_index=0):
        """
        Prints the tree directly, not a manipulable string.
        """
        print(self.tree_str(depth_index))
    
    def tree_str(self, depth_index=0, recursive_dict=None):
        """
        Returns the tree representation of a dictionary as a string.
        """
        if not hasattr(self,'iteritems'): return ''
        if recursive_dict is not None: self = TreeMap(recursive_dict)
        buff_str = ''
        
        for item in self.iteritems():
            # Starts working now.
            k = item[0]
            v = item[1]
            
            spacer = '\n' + '|     ' * depth_index
            
            if hasattr(v,'iteritems'):
                buff_str += spacer + '+--[ ' + k + ' ]'
                buff_str += self.tree_str(depth_index=depth_index + 1, recursive_dict=v)
            else:
                buff_str += spacer + '\_.--[ ' + str(k) + ' = ' + str(v) + ' ]'
        
        return buff_str
    
    def hash(self):
        """
        Starts gathering signatures at various levels, works based on 
        an already hierarchical dictionary. Signatures calculated are
        always one level less than the tree depth?
        
        This tries to separate signatures on the different level to look
        for similarities.
        """
        sign_map = AutoVivification()
        digest = lambda x: self.__polynomial_hash(x)
        # We are only doing signatures for top levels
        for k, v in self.iteritems():
            # Digested value of the string representation of 
            # what is behind.
            tmp = str(v)
            # Removed non meaningful information from the content.
            # No capital L is ever used in the register namings, so it is safe to strip that too.
            tmp = tmp.strip().replace('{','').replace('}','').replace(':','').replace(' ','').replace('L','')
            value = digest(tmp)
            sign_map[k] = string.atoi(value, 16)
        
        return sign_map
    
    def __polynomial_hash(self, s, base = 31, max_size=168):
        """
        Playing with different hashing algorithms to see what makes, more
        sense for fingerprints.
        
        http://www.csl.mtu.edu/cs2321/www/newLectures/16_Hash_Table.html
        
        Right now I am using polynomial hash codes as we care for the 
        characters itself in the tree with the errors that result from the
        system.
        
        Maybe a Locality Sensitive Hashing (LSH) algorithm is better suited
        for mapping close failures.
        """
        digest = 0
        max_size = 168
        for c in s: digest = base * digest  +  ord(c)
        digest &= 2 ** max_size - 1 
        return hex(digest).rstrip('L')
        
class AutoVivification(dict):
    """ Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

