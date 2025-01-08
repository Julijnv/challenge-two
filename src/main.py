import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from src.pdf_utils.extract import extract_text_from_pdf
from src.pipeline.lg_pipeline import run_pipeline_on_pdf
from src.storage.bigquery_insert import insert_into_bigquery

def ensure_dataset_exists(client, dataset_id):
    """Check if the dataset exists; if not, create it."""
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} already exists.")
    except NotFound:
        print(f"Dataset {dataset_id} not found. Creating it now...")
        dataset = bigquery.Dataset(dataset_id)
        client.create_dataset(dataset)
        print(f"Dataset {dataset_id} created successfully.")

def ensure_table_exists(client, table_id):
    """
    Check if the table exists; if not, create it with a predefined schema.
    table_id: 'project_id.dataset_id.table_name'
    """
    try:
        client.get_table(table_id) 
        print(f"Table {table_id} already exists.")
    except NotFound:
        print(f"Table {table_id} not found. Creating it now...")
        table = bigquery.Table(table_id, schema=[
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("authors", "STRING"),
            bigquery.SchemaField("publication_date", "STRING"),
            bigquery.SchemaField("abstract", "STRING"),
            bigquery.SchemaField("methodology_findings", "STRING"),
            bigquery.SchemaField("global_summary", "STRING"),
            bigquery.SchemaField("keywords", "STRING"),
        ])
        created = client.create_table(table)
        print(f"Table {created.full_table_id} created successfully.")

def main():
    pdf_path = "./papers/paper1.pdf"

    # BigQuery identifiers
    table_id = "horizontal-veld-446811-b8.paper_summarize1.papers"
    dataset_id = "horizontal-veld-446811-b8.paper_summarize1"


    client = bigquery.Client()

    ensure_dataset_exists(client, dataset_id)

    ensure_table_exists(client, table_id)

    final_data = run_pipeline_on_pdf(pdf_path, extract_text_from_pdf)

    insert_into_bigquery(final_data, table_id)

    query_str = f"SELECT * FROM `{table_id}` ORDER BY RAND() LIMIT 5"
    rows = client.query(query_str).result()

    print("\n--- Sample rows in BigQuery ---")
    for row in rows:
        print({
            "title": row.title,
            "authors": row.authors,
            "publication_date": row.publication_date,
            "abstract": row.abstract,
            "methodology_findings": row.methodology_findings,
            "global_summary": row.global_summary,
            "keywords": row.keywords
        })

if __name__ == "__main__":
    main()
