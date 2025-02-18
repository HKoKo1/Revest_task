This repository implements a Flask-based API that allows users to query a sales dataset using natural language. The system leverages the Langchain and Ollama/Google Gemini LLMs to convert the natural language queries into SQL, which is then executed on a DuckDB in-memory database.

Key Features:

1-Flask API: A RESTful API endpoint (/query) for querying the sales data.

2-DuckDB Integration: In-memory database to store and query the sales data from a CSV file (sales.csv).

3-Langchain + LLM: Utilizes Langchain and Ollama/Google Gemini LLM to convert natural language into SQL queries.

4-Error Handling: Logs errors and invalid SQL queries to ensure smooth operation.
