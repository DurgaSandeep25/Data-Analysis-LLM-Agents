import sqlite3
from typing import Any, Dict, List, Literal, Optional, Sequence, Union
import os
import pandas as pd

def get_custom_table_info(columns: List[str]) -> str:
    """
    Custom table information based on the input columns
    
    Args:
        columns: subset of columns/column names from the SQL table
    Returns:
        res: string, table information along with first 3 rows information.
    
    Example output: Observe how we are only providing information about few columns only
    
    CREATE TABLE fires (
        "SOURCE_SYSTEM" TEXT,
        "SOURCE_REPORTING_UNIT_NAME" TEXT,
        "FIRE_SIZE" FLOAT,
        "FIRE_SIZE_CLASS" TEXT,
        "STATE" TEXT,
        "FIPS_CODE" TEXT,
        "FIPS_NAME" TEXT
    )

    /*
    FIRE_SIZE	FIRE_SIZE_CLASS	STATE	FIPS_CODE	FIPS_NAME	SOURCE_REPORTING_UNIT_NAME	SOURCE_SYSTEM
    0.1	A	CA	063	Plumas	Plumas National Forest	FS-FIRESTAT
    0.25	A	CA	061	Placer	Eldorado National Forest	FS-FIRESTAT
    0.1	A	CA	017	El Dorado	Eldorado National Forest	FS-FIRESTAT
    */
    """
    # Connect to your database
    conn = sqlite3.connect('/project/pi_hongyu_umass_edu/zonghai/clinical-llm-alignment/durga_sandeep/Aira/submission/data/fires_database.db')
    cursor = conn.cursor()
    
    # Execute a query to retrieve table information
    cursor.execute("PRAGMA table_info(fires)")  # Change 'your_table' to your actual table name
    # Fetch the results
    table_info = cursor.fetchall()
    
    res = ""
    # Prepare the CREATE TABLE statement
    create_table_statement = "CREATE TABLE fires (\n"

    # Iterate over the table information and build the CREATE TABLE statement
    for column in table_info:
        column_name, data_type = column[1], column[2]
        if column_name not in columns:
            continue
        create_table_statement += f"\t\"{column_name}\" {data_type},\n"

    # Remove the trailing comma and newline
    create_table_statement = create_table_statement.rstrip(",\n")

    # Add the closing parenthesis
    create_table_statement += "\n)"
    res += create_table_statement
    
    # first 3 columns in the SQL table
    
    columns = ",".join(columns)
    
    # Execute a SELECT query to retrieve the desired information
    cursor.execute(f"SELECT {columns} FROM fires LIMIT 3")
    
    res += "\n\n/*\n"
    # Fetch the results
    rows = cursor.fetchall()
    
    # Print the column names
    column_names = [description[0] for description in cursor.description]
    res += '\t'.join(column_names) + "\n"

    # Print the data
    for row in rows:
        res += '\t'.join(map(str, row)) + '\n'
        
    res += "*/"
    # Close the connection
    conn.close()
    
    return res

def get_custom_sql_prompt(columns: List[str]) -> str:
    """
    Custom SQL Prompt with only selected columns information present
    
    Args:
        columns: subset of columns/column names from the SQL table
    Returns:
        system: string, final sql agent prompt
        
    """
    # get the custom table info
    custom_table_info = get_custom_table_info(columns)
    
    # final system prompt for the SQL agent
    system = """You are a {dialect} expert. Given an input question, creat a syntactically correct {dialect} query to run.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use date('now') function to get the current date, if the question involves "today".

    Only use the following tables: {table_info}
    """
    system += custom_table_info

    system += """

    Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins

    Use format:

    First draft: <<FIRST_DRAFT_QUERY>>
    Final answer: <<FINAL_ANSWER_QUERY>>
    """
    
    return system