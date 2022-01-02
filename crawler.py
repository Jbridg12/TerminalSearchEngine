'''
Josh Bridges
crawler.py

A Web Crawler that retrieves all 'utk.edu' links up to a provided depth from a root url.
Then reads each url into a document string and cleans the strings. All results are
stored in the Links and Docs lists
'''
import requests
import certifi
import ssl
import string
from socket import timeout
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

class WebCrawler:
    def __init__(self, root, verbose):  
        '''Constructor for the Web Crawler class
        
        Keyword arguments:
        root -- a url to a website to begin the webcrawling from
        verbose -- boolean to specify command line verbosity
        '''
        self.root = root
        self.verbose = verbose
        self.hdr = {'User-Agent': 'Mozilla/5.0'}    # Set headers for http requests
        self.docs = []
        self.links = []
        
    def get_documents(self):    
        '''Returns the list of cleaned documents.'''
        return self.docs
    def set_documents(self, d):
        '''Sets the list of cleaned documents.'''
        self.docs = d
    def get_links(self):        
        '''Returns the list of collected links'''
        return self.links
    def set_links(self, l):     
        '''Sets the list of collected links.'''
        self.links = l
    def collect(self, s, d):    
        '''Collects the list of links starting with site s and “hopping” a depth of d.
        
        Keyword arguments:
        s -- a url to a website
        d -- the depth from s to collect links
        '''
        if self.verbose:
            print("[VERBOSE] 1. COLLECTING LINKS - STARTED")
        links = [[s]]
        count = 1
        
        # Loop over each depth
        for l in range(d+1):
            links.append([])
            
            # Loop over all links for each depth
            for site in links[l]:
                req = Request(site, headers=self.hdr)
                
                # Try each url connection a maximum of 10 times
                for i in range(10):
                
                    # The following try statement catches and prints any HTTP error that BeautifulSoup 
                    # encounters when opening the website at the URL.
                    try:
                        page = urlopen(req, timeout=10, context=ssl.create_default_context(cafile=certifi.where()))
                        soup = BeautifulSoup(page, 'html.parser')
                        
                        # Find each link in the document
                        for k in soup('a'):
                            # Check if there is a url stored in 'href'
                            if k.has_attr('href'):
                                # Parse the url and check to make sure it ends in utk.edu
                                domain = urlparse(k['href']).netloc
                                domains = domain.split('.')
                                if len(domains) < 2:
                                     continue
                                     
                                if domains[-2] == "utk" and domains[-1] == "edu":
                                    # Check if the url is already in the links list
                                    if k['href'] not in [item for sublist in links for item in sublist]:
                                        if self.verbose:
                                            print("[VERBOSE] COLLECTED LINK (" + str(count) + ")")
                                        count += 1
                                        
                                        # Add link to the next depth list
                                        links[l+1].append(k['href'])
                    except HTTPError as err:
                        print(err.code)
                        continue
                    except URLError as err:
                        print (err.reason)
                        continue
                    except timeout as err:
                        print("Connection timed out.")
                        continue
                    break
                    
        # Flatten the links list to a single list
        flat_links = [item for sublist in links for item in sublist]
        if self.verbose:
            print("[VERBOSE] 1. COLLECTING LINKS - DONE")
        return flat_links
        
    def crawl(self):            
        '''Extracts and stores all relevant text from the list of collected links.'''
        
        if self.verbose:
            print("[VERBOSE] 2. CRAWLING LINKS - STARTED")
            
        good_links = []
        
        # Loop over each link in the list
        for i, site in enumerate(self.links):
            if self.verbose:
                print("[VERBOSE] CRAWLING: LINK (" + str(i+1) + "/" + str(len(self.links)) + ")")
            
            req = Request(site, headers=self.hdr)
            paragraphs = []
            
            for z in range(10):
                # The following try statement catches and prints any HTTP error that BeautifulSoup 
                # encounters when opening the website at the URL.
                try:
                    page = urlopen(req, timeout=10, context=ssl.create_default_context(cafile=certifi.where()))
                    soup = BeautifulSoup(page, 'html.parser')
                    
                    # Collect all paragraphs from specified sections and tables
                    for j in soup.find_all('div', {'class':'person-content', 'class' : 'entry-content'}):
                        for i in soup('p'):
                            paragraphs.append(i.text)
                    for t in soup('table', {'class' : 'table_default'}):
                        paragraphs.append(t.text)
                        
                except HTTPError as err:
                    print(err.code)
                    continue
                except URLError as err:
                    print (err.reason)
                    continue
                except timeout as err:
                    print("Connection timed out.")
                    continue
                break
                
            # Insert text as a string into docs list
            self.docs.append(' '.join(paragraphs))
        if self.verbose:
            print("[VERBOSE] 2. CRAWLING LINKS - DONE")
        return
        
    def clean(self):            
        '''Modifies text extracted from webpages. Returns the cleaned documents in a list.'''
        if self.verbose:
            print("[VERBOSE] 3. CLEANING TEXT - STARTED")
        
        # Clean each doc in the list
        cleaned_docs = []
        for doc in self.docs:
            # Remove unicode characters
            ascii_only = doc.encode("ascii", "ignore").decode()
            
            # Remove all @texts in the page
            pat = r'(@\w+)'
            no_handles = ascii_only.replace(pat, "")
            
            # Remove all punctuation from the document
            no_punc = no_handles.translate(str.maketrans('','',string.punctuation))
            
            # Remove double spaces and change all to lowercase
            no_double_space = no_punc.replace("  ", " ")
            lowercase = no_double_space.lower()
            
            cleaned_docs.append(lowercase)
            
        # Change docs list to the new, cleaned documents
        self.docs = cleaned_docs
        if self.verbose:
            print("[VERBOSE] 3. CLEANING TEXT - DONE")
        return

