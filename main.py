import logging
from flask import Flask, request, jsonify, render_template
import duckdb
import pandas as pd
from langchain.llms import Ollama
import re



# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)

# Load the dataset into DuckDB
csv_file = "sales.csv"  # Ensure this file exists in the same directory
df = pd.read_csv(csv_file)
df.head()


# Check if the dataset is loaded correctly
if df.empty:
    logger.error("Error: sales.csv is empty or not loaded correctly.")
    raise RuntimeError("sales.csv is empty or missing.")

# Initialize DuckDB
try:
    duckdb_conn = duckdb.connect(database=':memory:', read_only=False)
    duckdb_conn.execute("DROP TABLE IF EXISTS sales")
    duckdb_conn.execute("CREATE TABLE sales AS SELECT * FROM df")
    logger.info("Database loaded with sales data")
except Exception as e:
    logger.error(f"DuckDB initialization error: {e}")
    raise RuntimeError("Failed to initialize DuckDB.")

# Initialize Ollama LLM
# llm = Ollama(base_url='http://localhost:11434', model='llama3.2')

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyBAULyA9-fLy-zcqaHkdzOBABUucJr5pBs", temperature=0.7)


logger.info("Ollama LLM initialized")

# Function to generate SQL query using LLM
def generate_sql(question: str) -> str:
    logger.debug(f"Received question: {question}")

    prompt = f"""
    You are an expert SQL assistant. Convert the given natural language query into a valid SQL query.

    The table 'sales' has these columns:
    {', '.join(df.columns)}

    Follow these rules:
    
    - Use `sales` as the table name.
    - Always return a properly formatted SQL query.
    - Do NOT include markdown-style code blocks (e.g., ```sql ... ```).
    - Do NOT use words like `To`, `TABLE`, `DROP`, or `DELETE`.
    - Return only the SQL query, nothing else.

    Natural Language Query: "{question}"
    
    SQL Query:
    """
    
    response = llm.invoke(prompt)  # Get AIMessage object
    sql_query = response.content.strip()  # Extract text from AIMessage

    # Remove markdown-style code blocks if present
    sql_query = re.sub(r'```sql|```', '', sql_query).strip()
    
    logger.debug(f"Generated SQL Query: {sql_query}")  # Print SQL to terminal
    
    return sql_query


# Define API endpoint
@app.route("/query", methods=["POST"])
def query_data():
    try:
        data = request.json
        question = data.get("question")
        logger.info(f"Received API request with question: {question}")
        sql_query = generate_sql(question)
        
        if "TABLE" in sql_query.upper() or "DROP" in sql_query.upper() or "DELETE" in sql_query.upper():
            logger.error(f"Invalid SQL detected: {sql_query}")
            return jsonify({"error": "Generated SQL is invalid."}), 400

        logger.info(f"Executing SQL query: {sql_query}")
        result = duckdb_conn.execute(sql_query).fetchdf()
        logger.info("Query execution successful, returning results")
        return jsonify({"sql": sql_query, "result": result.to_dict(orient='records')})
    except duckdb.Error as db_err:
        logger.error(f"DuckDB Error: {db_err}")
        return jsonify({"error": f"DuckDB Error: {str(db_err)}"}), 400
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return jsonify({"error": f"Error: {str(e)}"}), 400

# Root endpoint for API welcome message
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
