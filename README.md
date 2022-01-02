# Search Engine
This folder contains four python files and two .pickle files. The .pickle files are csv files of the documents and links of the pretrained depth one
results. The three class files interface.py, crawler.py, and engine.py provide the documented code for each class. 
The main.py file contains the driver code and is the file that needs to be called on the command line.

This program searches the URL provided in ROOT and collects links for a depth of 1 (by default). This means each link from the 
ROOT is searched. Each link has their text extracted and then vectorized and stored. The user can then search the texts for 
the closest matching documents for their query. The similarity is determined by cosine similarity and the top 5 results are printed out.

There are two options for mode, {C : Command Line, I : Interactive Interface}. That change the user experience
with the search engine. 


# Dependencies
	Numpy
	Pandas
	Sklearn (Scikit-Learn)
	CSV
	ArgParse
	Certifi
	SSL
	BeautifulSoup4


# Usage
The search engine is started by running the following command in the directory
	>python main.py -root ROOT -mode [C, I] -query QUERY -verbose [T, F]
	
ROOT and MODE are required arguments and the execution changes based on the specified Mode.

If mode is specified as 'C' then the user must provide the -query argument in the command line as well.
This mode prints the top 5 urls to the terminal for the provieded query.

If mode is specified as 'I' then the interactive interface starts and the user can use 4 input options:
	:exit	- quit the interactive interface
	:delete	- delete the local .pickle files in the directory
	:train	- retrieve the urls and docs and setup the search engine for use
	query	- any other string provided gets parsed as a serach term and the top 5 matching urls are provided


# Submission Info
- Josh Bridges
- jbridg12
- 11/30/2021
