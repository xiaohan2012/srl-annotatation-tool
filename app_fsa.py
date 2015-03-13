"""
Finite State Automaton
"""
from trie_fsa import TrieFSA
from op import (Label, CancelLabel, 
                CursorLeft, CursorRight, CursorUp, CursorDown, 
                ConfirmSentence, SetMark)

class AppConfigError(Exception):
    pass

class AppFSA(TrieFSA):
    """
    FSA for this app

    >>> from test_config import config
    >>> fsa = AppFSA.from_config(config)
    >>> fsa.take('j')
    >>> fsa.can_terminate
    True
    >>> fsa.ops #doctest: +ELLIPSIS
    [<op.CursorLeft object at ...>]
    >>> fsa.reset()
    >>> fsa.take('p')    
    >>> fsa.take('r')
    >>> fsa.can_terminate
    False
    >>> fsa.take('o')
    >>> fsa.can_terminate
    True
    >>> print fsa.ops #doctest: +ELLIPSIS
    [Label(role, problem)]
    """
    
    @classmethod
    def from_config(cls, config):
        fsa = AppFSA()
        for key in config:
            if key == "labels":
                for group, group_labels in config[key].items():
                    fsa.add_paths(group_labels, 
                                  lambda label: Label(group, label))
                        
            else:
                if key in globals():
                    op = globals()[key]
                    value = config[key]
                    if not isinstance(value, basestring):# an int
                        value = [value]
                    fsa.add_paths([value], last_value_func = lambda _: op())
                else:
                    raise AppConfigError("Invalid operator name %s" %(key))

        return fsa

    @property
    def ops(self):
        """get all the operations starting from the current state"""
        return [op for path, op in self.matching_paths()]

    @property
    def can_terminate(self):
        """If the current state leads to only one terminal state
        """
        return len(self.ops) == 1
