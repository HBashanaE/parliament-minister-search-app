# Parliament Ministers Search Engine

- A Sinhala search engine implemented using ElasticSearch and Python
- The project is developed as the IR project CS4642 Data Mining and Information Retrieval under the supervision of Dr.U.Thayasivam at University of Moratuwa.


### Setting up ElasticSearch

On this project, Elasticsearch is run on the localhost. Elasticsearch can be downloaded from the [official website](https://www.elastic.co/downloads/elasticsearch).
After extracting the downloaded zip file, run ./elasticsearch (elasticseach on Windows) from bin folder. This will bring up the ElasticSearch server on default port 9200.

### Data

Data for this project is obtained from [parliament.lk](https://www.parliament.lk/si/members-of-parliament/directory-of-members/). Metadata used are the name of the minister, the political party of the minister, the electoral district of the minister, date of birth of the minister, civil status of the minister, the religion of the minister, position of the minister in parliament (if applicable), profession of the minister (if applicable) and committees represented by the minister. 

1. Scraping
  - The scraping of the web pages is done by using the BeautifulSoup Python library.

2. Data Cleaning & Preprocessing
  - Need for data cleaning was minimal as data was originally in Sinhala Unicode without errors. However, removing whitespaces was needed when data is scraped and structured.
  
### Creating Indexes on ElasticSearch

To create indexes on ElasticSearch, elasticsearch python package was used.

### Advanced Features
1. Query intent classification
  - Simple rule-based approach was followed to classify the intent of the query. Specific words in the user query were used to classify the intent of the query. This helped to improve the precision of the system.
  
2. Range queries
  - Range queries were used to retrieve age-related information.

### Frontend & Backend

1. Frontend

  - Frontend is implemented using Flask's default templating engine with HTML, JQuery and Materialize CSS library.

2. Backend

  - The backend is implemented using the Python Flask framework. Backed is used to retrieve data from ElasticSearch endpoints and serve the frontend