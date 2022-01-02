'''
Josh Bridges
interface.py

A Search Interface that has two modes:
    Command line - Pass user provided query to search engine one time
    Interface    - Format prompts to recieve user input repeatedly 

'''
import sklearn
import engine

class SearchInterface:
    def __init__(self, mode, engine, query):
        '''Constructor for Search Interface class
        
        Keyword arguments:
        mode  -- C or I specifying command-line mode or interface mode respectively
        engine -- an instance of the Search Engine class
        query -- user provided string that's either a command or a search
        '''
        self.mode = mode
        self.engine = engine
        self.query = query
    def listen(self):
        ''' If user specified Console mode then take the provided query and parse it.
            Otherwise create the interactive search interface and parse user input.
        '''
        
        # In console mode just parse the individual query
        if self.mode == 'C':
            self.engine.handle_query(self.query) 
        # Interface mode needs to loop for user input
        else:
            # Format search engine header
            print('-----------------------------------')
            print('|         UTK EECS SEARCH         |')
            print('-----------------------------------')
            
            # Loop for user input
            while True:
                q = input('>')
                
                # Specify exit condition
                if q == ':exit':
                    break
                
                self.handle_input(q)
        return
    def handle_input(self, query):  
        '''Check the user specified input and call the proper methods
        
        Keyword arguments:
        query -- user provided string that's either a command or a search
        '''
        
        # If query is a command then call the proper SearchEngine method
        if query == ':delete':
            self.engine.delete()
            return
        elif query == ':train':
            self.engine.train()
            return
        # Otherwise perform a search with the parsed query
        else:
            self.engine.handle_query(query)