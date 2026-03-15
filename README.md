# Stocks Serverless Pipeline
## Description
Checks a list of tech stocks to see which one moved the most daily. Saves result and shows the last 7 days on a webpage. 

### Technologies Used
Serverless Framework
AWS / Python / HTTP API template
AWS Services: Lambda, API Gateway, EventBridge, DynamoDB, S3 

### Repository Structure
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