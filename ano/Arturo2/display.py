#  _____     _               
# |  _  |___| |_ _ _ ___ ___ 
# |     |  _|  _| | |  _| . |
# |__|__|_| |_| |___|_| |___|
# http://32bits.io/Arturo/
#
from distutils.util import strtobool
import string

from ano.Arturo2 import ArgumentVisitor


# +---------------------------------------------------------------------------+
# | Console
# +---------------------------------------------------------------------------+
class Console(ArgumentVisitor):
    
    INDENTATION = "    "
    
    def __init__(self, indents=0):
        super(Console, self).__init__()
        self._loglevel = 0
        self._contexts = []
        self._indents = indents
        self._indent = ""
        self._resetIndent()
        
    def shift(self):
        '''
        Increase console indentation by 1.
        '''
        self._indents += 1
        self._resetIndent()
    
    def unshift(self):
        '''
        Decrease console indendataion by 1.
        '''
        if self._indents > 0:
            self._indents -= 1
            self._resetIndent()

    def pushContext(self):
        '''
        Push the current state of the console into the context stack and expose a new set of states. Use
        push/popContext to handle restoring the original context when an exception is thrown. For example:
        
            try:
                console.pushContext()
                ...
            finally:
                console.popContext()
        '''
        # For now context==indentation but this may change in the future.
        self._contexts.append(self._indents)
        
    def popContext(self):
        '''
        Pop the last console state from the context stack and restore.
        '''
        # For now context==indentation but this may change in the future.
        if len(self._contexts) > 0:
            currentIndents = self._indents
            self._indents = self._contexts.pop()
            if currentIndents != self._indents:
                self._resetIndent()

    def printVerbose(self, message):
        if self._loglevel > 1:
            self._printMessage(message)
            
    def printDebug(self, message):
        if self._loglevel > 0:
            self._printMessage(message)
        
    def printInfo(self, message):
        self._printMessage(message)
        
    def printWarning(self, message):
        self._printMessage(message)
        
    def askYesNoQuestion(self, question):
        response = raw_input(self._indent + self._colourize(question, 'red'))
        return strtobool(response)

    # +---------------------------------------------------------------------------+
    # | ArgumentVisitor
    # +---------------------------------------------------------------------------+
    def onVisitArgParser(self, parser):
        parser.add_argument('-v', '--verbose',
                            default=False,
                            action='store_true',
                            help=_('Enable verbose logging.'))

    def onVisitArgs(self, args):
        if getattr(args, "verbose"):
            self._loglevel = 2
            self.printVerbose(_('enabling verbose logging.'))
    
    # +---------------------------------------------------------------------------+
    # | PRIVATE
    # +---------------------------------------------------------------------------+
    def _resetIndent(self):
        self._indent = ""
        for i in range(0, self._indents):  # @UnusedVariable
            self._indent += Console.INDENTATION
            
    def _printMessage(self, message):
        print self._indent + message

    def _colourize(self, text, colour):
        if string.lower(colour) in ('red'):
            return "\x1b[31m" + text + "\x1b[0m"
        return text