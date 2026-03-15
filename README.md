# Stocks Serverless Pipeline

## Description

Checks a list of tech stocks to see which one moved the most daily. Saves result and shows the last 7 days on a webpage. 

### Technologies Used

Serverless Framework
AWS / Python / HTTP API template
AWS Services: Lambda, API Gateway, EventBridge, DynamoDB, S3 

### AWS Architecture 

![AWS Architecture Diagram](/architecture_diagram.png)
EventBridge triggers a daily ingestion Lambda that fetches stock data from the Massive API, computes the top mover, and stores the result in DynamoDB. A static frontend hosted on S3 calls the GET /movers API Gateway endpoint, which invokes a retrieval lambda to return the results of the last 7 days. 

### Repository Structure

```
├── backend
│   ├── handlers
│   │   ├── ingest.py
│   │   └── retrieve.py
│   ├── requirements.txt
│   └── services
│       ├── db.py
│       ├── mover_logic.py
│       └── stock_api.py
├── frontend
│   ├── app.js
│   ├── index.html
│   └── styles.css
└── serverless.yml
```