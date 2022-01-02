'''
Josh Bridges
engine.py

A Search Engine that matches a user provided query with cleaned web pages based
on their cosine similarity. Prints best 5 matchin urls to the console.

'''

import crawler
import interface
import os
import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer 

class SearchEngine:
    def __init__(self, mode, verbose, query, root, depth):  
        '''Constructor for the Search Engine class
        
        Keyword arguments:
        mode  -- C or I specifying command-line mode or interface mode respectively
        verbose -- boolean to specify command line verbosity
        query -- user provided string that's either a command or a search
        root -- a url to a website to begin the webcrawling from
        depth -- integer specifying how many links deep the crawler will search
        '''
        
        self.mode = mode
        self.verbose = verbose
        self.query = query
        self.root = root
        self.depth = depth
        self.crawler = crawler.WebCrawler(root, verbose)                # Instantiate a WebCrawler object
        self.interface = interface.SearchInterface(mode, self, query)   # Instantiate a Search Interface object
        self.tfidf_frame = None                                         # Store the dataframe from tfidf vectorizer 
        self.vectorizer = None                                          # The vectorizer object from tfidf vectorizer 
        

        self.train()                                                    # Calls self.train() at the end of init to ensure training before execution 
        
    def train(self):
        '''If the .pickle files already exist then read the files into the crawlers lists docs and links. 
            Otherwise perform the Collect, Crawl, and Clean methods and store the retrieved information in docs.pickle
            and links.pickle
        '''
        
        # Make sure relevant lists are empty
        self.crawler.docs = []
        self.crawler.links = []
        
        # Check if .pickle files already exist
        if os.path.isfile('./docs.pickle') and os.path.isfile('./links.pickle'):
            
            # Since these .pickle files are in csv format, parse them with csv module
            with open('docs.pickle', 'r', newline='') as dp:
                for doc in csv.reader(dp, delimiter=','):
                    self.crawler.docs.append(doc)
            with open('links.pickle', 'r', newline='') as lp:
                for link in csv.reader(lp, delimiter=','):
                    self.crawler.links.append(link)
                   
                   
            # Set local lists to flattened csv results
            self.crawler.set_documents([item for sublist in self.crawler.docs for item in sublist])
            self.crawler.set_links([item for sublist in self.crawler.links for item in sublist])
        
        # If the files DO NOT exist
        else:
            # Perform all crawler methods to retriieve links and docs
            self.crawler.set_links(self.crawler.collect(self.root, self.depth))
            self.crawler.crawl()
            self.crawler.clean()
            
            # Write the results to the 2 pickle files
            with open('docs.pickle', 'w', newline='') as dp:
                dr = csv.writer(dp, quoting=csv.QUOTE_ALL)
                dr.writerow(self.crawler.docs)
                
            with open('links.pickle', 'w', newline='') as lp:
                lr = csv.writer(lp, quoting=csv.QUOTE_ALL)
                lr.writerow(self.crawler.links)
                
        # Vectorize the documents
        self.tfidf_frame = self.compute_tf_idf()
        return
        
    def delete(self):
        ''' Delete existing .pickle files in the local directory
        '''
        if os.path.isfile('./docs.pickle'):
            os.remove('./docs.pickle')
        if os.path.isfile('./links.pickle'):
            os.remove('./links.pickle')
            
    def compute_tf_idf(self):
        ''' Vectorize the documents using TFIDFvectorizer and return results in
            a DataFrame indexed by vocabulary
        '''
        # Instantiate the Tfidfvectorizer
        tfidf_vectorizer = TfidfVectorizer() 
        
        # Send our docs into the Vectorizer
        tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(self.crawler.docs)
        
        # Transpose the result into a more traditional TF-IDF matrix, and
        # convert it to an array.
        X = tfidf_vectorizer_vectors.T.toarray()
        
        # Convert the matrix into a dataframe using feature names as the 
        # dataframe index.
        self.vectorizer = tfidf_vectorizer
        return pd.DataFrame(X, index=tfidf_vectorizer.vocabulary_)
        
    def handle_query(self, query):
        ''' Compute cosine similarity between query and the cleaned docs and print the
            top 5 urls that match the query.
            
            Keyword arguments:
            query -- user provided search term
        '''
        # [ RETRIEVAL STAGE ]
        # Vectorize the query.
        q = [query]
        q_vec = self.vectorizer.transform(q).toarray().reshape(self.tfidf_frame.shape[0],)
        
        # Calculate cosine similarity.
        sim = {}
        for i in range(len(self.tfidf_frame.columns)-1):
        
            # If dividing by 0 set similarity to 0
            if np.linalg.norm(self.tfidf_frame.loc[:, i]) * np.linalg.norm(q_vec) == 0:
                sim[i] = 0
            else:
                sim[i] = np.dot(self.tfidf_frame.loc[:, i].values, q_vec) / (np.linalg.norm(self.tfidf_frame.loc[:, i]) * np.linalg.norm(q_vec))
           
        # Sort the values 
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
        
        # Print the URLs and their similarity values
        i = 0
        for k, v in sim_sorted:
            if v != 0.0 and i < 5:
                print("["+ str(k)+ "] " + str(self.crawler.get_links()[k])+ '(' + str("{:.2f}".format(v)) + ')')
                i += 1
               
    def listen(self):
        ''' Call interface method to read user input'''
        self.interface.listen()