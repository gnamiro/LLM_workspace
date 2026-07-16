from __future__ import annotations

import os

import duckdb
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    duckdb_path = os.getenv("LOGFIRE_DUCKDB_PATH", "logfire.duckdb")
    dataset_name = os.getenv("LOGFIRE_DATASET_NAME", "agent_traces")
    query = """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = ?
    """

    with duckdb.connect(duckdb_path) as conn:
        table_count = conn.execute(query, [dataset_name]).fetchone()[0]
        print(table_count)


if __name__ == "__main__":
    main()
