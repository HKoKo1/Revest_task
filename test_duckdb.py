import duckdb
import pandas as pd

# Load CSV into a DataFrame
csv_file = "sales.csv"  # Ensure the file exists
df = pd.read_csv(csv_file)

# Connect to DuckDB (in-memory database)
conn = duckdb.connect(database=':memory:', read_only=False)

# Create a table in DuckDB
conn.execute("DROP TABLE IF EXISTS sales")
conn.execute("CREATE TABLE sales AS SELECT * FROM df")

print("✅ Database loaded successfully!")

# Test Queries
try:
    # Fetch first 5 rows
    result = conn.execute("SELECT * FROM sales LIMIT 5").fetchdf()
    print("\n🔹 First 5 rows of the sales table:")
    print(result)

    # Get total sales for Furniture category
    total_sales = conn.execute("SELECT SUM(Sales) FROM sales WHERE Category = 'Furniture'").fetchall()
    print(f"\n🔹 Total Sales for 'Furniture' category: {total_sales[0][0]}")

    # Count the number of orders
    order_count = conn.execute("SELECT COUNT(*) FROM sales").fetchall()
    print(f"\n🔹 Total number of orders: {order_count[0][0]}")

except Exception as e:
    print(f"❌ Error executing query: {e}")

# Close the connection
conn.close()
print("\n✅ Test complete. Database connection closed.")
