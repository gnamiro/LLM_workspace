from __future__ import annotations

import os

import duckdb
from dotenv import load_dotenv

load_dotenv()


def _pick_column(columns: set[str], *candidates: str) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def main() -> None:
    duckdb_path = os.getenv("LOGFIRE_DUCKDB_PATH", "logfire.duckdb")
    dataset_name = os.getenv("LOGFIRE_DATASET_NAME", "agent_traces")
    trace_id = os.getenv("LOGFIRE_TRACE_ID")
    table_name = f"{dataset_name}.query"

    where_clause = ""
    params: list[str] = []
    if trace_id:
        where_clause = "WHERE trace_id = ?"
        params.append(trace_id)

    with duckdb.connect(duckdb_path) as conn:
        column_rows = conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
        columns = {row[1] for row in column_rows}

        input_col = _pick_column(
            columns,
            "gen_ai_usage_input_tokens",
            "attributes__gen_ai_usage_input_tokens",
            "attributes__gen_ai_aggregated_usage_input_tokens",
        )
        output_col = _pick_column(
            columns,
            "gen_ai_usage_output_tokens",
            "attributes__gen_ai_usage_output_tokens",
            "attributes__gen_ai_aggregated_usage_output_tokens",
        )
        operation_col = _pick_column(
            columns,
            "gen_ai_operation_name",
            "attributes__gen_ai_operation_name",
        )

        if input_col is None:
            raise RuntimeError(
                f"Couldn't find an input-token column in {table_name}. "
                f"Available token-like columns: "
                f"{sorted(c for c in columns if 'token' in c or 'gen_ai' in c)}"
            )

        llm_filter = ""
        if operation_col:
            llm_filter = (
                f"{'AND' if where_clause else 'WHERE'} "
                f"{operation_col} IN ('chat', 'responses')"
            )

        query = f"""
            SELECT
                trace_id,
                COUNT(*) AS span_count,
                SUM(COALESCE({input_col}, 0)) AS input_tokens,
                SUM(COALESCE({output_col or '0'}, 0)) AS output_tokens
            FROM {table_name}
            {where_clause}
            {llm_filter}
            GROUP BY trace_id
            ORDER BY input_tokens DESC
        """

        rows = conn.execute(query, params).fetchall()
        if not rows:
            print("No matching traces found.")
            return

        for row in rows:
            print(
                f"trace_id={row[0]} span_count={row[1]} "
                f"input_tokens={row[2]} output_tokens={row[3]}"
            )


if __name__ == "__main__":
    main()
