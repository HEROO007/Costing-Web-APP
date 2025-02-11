try:
    import streamlit as st
    import pandas as pd
    import sqlite3
    import sys
except ModuleNotFoundError as e:
    st.error(f"Missing module: {e.name}. Please install it using 'pip install {e.name}'.")
    sys.exit(1)

# Title of the app
st.title("Excel to Web App")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("### Preview of Data:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
    
    # Save to SQLite
    try:
        conn = sqlite3.connect("sales_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                product TEXT,
                target INTEGER,
                sales INTEGER
            )
        """)
        conn.commit()
        
        # Insert data
        for _, row in df.iterrows():
            cursor.execute("INSERT INTO sales (order_id, product, target, sales) VALUES (?, ?, ?, ?)",
                           (row.get("order_id"), row.get("product"), row.get("target"), row.get("sales")))
        conn.commit()
        conn.close()
        
        st.success("Data saved to database!")
    except Exception as e:
        st.error(f"Database error: {e}")

# Show stored data
if st.button("Show Stored Data"):
    try:
        conn = sqlite3.connect("sales_data.db")
        df_db = pd.read_sql("SELECT * FROM sales", conn)
        conn.close()
        st.write("### Data from Database:")
        st.dataframe(df_db)
    except Exception as e:
        st.error(f"Error fetching data from database: {e}")
