[![Build Status](https://travis-ci.com/elben10/ScrapingClass.svg?branch=master)](https://travis-ci.com/elben10/ScrapingClass)
# ScrapingClass

## Installation

Last published version
`pip install scraping_class`

Development version
`pip install git+https://github.com/elben10/ScrapingClass`

## Use

First we import the module and initiates the `Connector` class, and choose a file to write the log to.
```python
import scraping_class
conn = scraping_class.Connector(logfile="log.csv", overwrite_log=True)
```

The code above creates a csv file named `log.csv` which looks like this

| id | project | connector_type | t | delta_t | url | redirect_url | response_size | response_code | success | error | 
|----|---------|----------------|---|---------|-----|--------------|---------------|---------------|---------|-------| 



Then we make a requests for Github API.

```python
url = "https://api.github.com/"
response, id_ = conn.get(url, "")
```

The `reponse` is a requests response, and the `id_` is a request counter. Now the log file looks like this

| id | project | connector_type | t | delta_t | url | redirect_url | response_size | response_code | success | error | 
|----|---------|----------------|---|---------|-----|--------------|---------------|---------------|---------|-------| 
| 0 |  | requests | 1565947269.012394 | -0.8160951137542725 | https://api.github.com/ | https://api.github.com/ | 2039 | 200 | True |  | 
