import re
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

def extract_sql_query(text: str) -> str:
    
    """
    Post-processing of SQL raw query
    
    Args:
        text: str, Raw SQL query that might contain special token `sql`
    Returns:
        output: string, valid SQL query
    """
    
    # Define the regular expression pattern to match SQL queries
    pattern = r'```sql\n(.*?)```'
    # Use re.findall() to find all matches of the pattern in the text
    matches = re.findall(pattern, text, re.DOTALL)
    # Return the first match (assuming there's only one SQL query in the text)
    if matches:
        return matches[0]
    else:
        
        idx = text.lower().find("select")
        
        return text[idx:]