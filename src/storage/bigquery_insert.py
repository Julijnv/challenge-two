from google.cloud import bigquery

def insert_into_bigquery(data: dict, table_id: str):
    """
    Inserts a single record (dictionary) into a BigQuery table.
    """
    client = bigquery.Client()

    row_to_insert = {
        "title": data.get("title", ""),
        "authors": data.get("authors", ""),
        "publication_date": data.get("publication_date", ""),
        "abstract": data.get("abstract", ""),
        "methodology_findings": data.get("methodology_findings", ""),
        "global_summary": data.get("global_summary", ""),
        "keywords": ",".join(data["keywords"]) if isinstance(data["keywords"], list) else ""
    }
    
    errors = client.insert_rows_json(table_id, [row_to_insert])
    if not errors:
        print(f"Inserted data into {table_id}")
    else:
        print(f"Encountered errors while inserting rows: {errors}")
