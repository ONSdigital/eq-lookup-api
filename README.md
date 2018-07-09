# eQ Lookup API

EQ Lookup API provides a simple request service that will return a list of results.

First, clone the repo:
  ```bash
   $ git clone https://github.com/ONSdigital/eq-lookup-api.git
   ```
 
## Run in a virtual environment
- Make sure you have a working `pipenv` installation.
- Install dependencies, activate virtual environment and run:
  ```bash
   $ cd eq-lookup-api
   $ pipenv install --dev
     ...
   $ pipenv shell
     Spawning environment shell (/bin/bash). Use 'exit' to leave.
     ...
   $ FLASK_APP=application.py LOOKUP_URL='lookup_url' flask run
   [2018-04-10 14:05:11.419541] INFO: app: Logging configured
    * Serving Flask app "application"
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)   
  ```

## Usage
To browse the API navigate a browser to `http://localhost:5000`.  You will be given the search options.

To search for a Country: `http://localhost:5000/country/?q=CountryName` (i.e `country/?q=United`)


### Notes
- The `q` parameter is ignored when requesting the root resource.