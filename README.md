# Askbot
This is a simple Python and HTML code for building your own chatbot using rule-based data. 

## Data 
Requires a relational database (RDB) such as MySQL for the demo. 
The database should include the following columns: "request," "rules," and "response." 
Each attribute serves the following purpose:

```
1. request : Full sentence of the requests made by users
2. rules : specific words or phrases that will be used to fetch and identify the appropriate response. Each rule or word is delimited by '|'
3. Response : The most suitable answer or response for the corresponding request.
```

## Python
```
Framework : flask
Library : pandas
```

## Next Step
There are only 2 pages which are ask and adding data. To build proper Askbot, users and admins should distiguished in different page with different purposes
