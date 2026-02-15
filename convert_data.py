import duckdb
import os

# Define paths
CSV_PATH = "/Users/justinkao/Downloads/national_single/national_single.csv"
PARQUET_PATH = "epa_facilities.parquet"

def convert_csv_to_parquet():
    """Converts the national_single.csv to Parquet format using DuckDB."""
    print(f"Reading from: {CSV_PATH}")
    
    if not os.path.exists(CSV_PATH):
        print(f"Error: File not found at {CSV_PATH}")
        return

    try:
        # Use DuckDB to read CSV and write to Parquet directly
        # We perform some basic cleaning/renaming if needed, but selecting * is fine for now
        # We wrap column names in double quotes to handle spaces or special chars if any
        query = f"""
            COPY (
                SELECT * FROM read_csv_auto('{CSV_PATH}', ignore_errors=true)
            ) TO '{PARQUET_PATH}' (FORMAT 'PARQUET', CODEC 'SNAPPY');
        """
        
        con = duckdb.connect()
        con.execute(query)
        print(f"Successfully created {PARQUET_PATH}")
        
        # Verify row count
        count = con.execute(f"SELECT COUNT(*) FROM '{PARQUET_PATH}'").fetchone()[0]
        print(f"Total rows in Parquet: {count}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    convert_csv_to_parquet()
