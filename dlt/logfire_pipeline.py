from __future__ import annotations

import os

import dlt
from dotenv import load_dotenv
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources

load_dotenv()

DEFAULT_BASE_URL = "https://logfire-us.pydantic.dev/v1/"
DEFAULT_SQL = "select * from records"


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _optional_env(name: str) -> str | None:
    value = os.getenv(name)
    return value if value else None


@dlt.source(name="logfire_api")
def logfire_source(
    read_token: str = dlt.secrets.value,
    base_url: str = DEFAULT_BASE_URL,
    sql: str = DEFAULT_SQL,
    limit: int = 1000,
    json_rows: bool = True,
    min_timestamp: str | None = None,
    max_timestamp: str | None = None,
    timezone: str | None = None,
):
    params: dict[str, object] = {
        "sql": sql,
        "limit": limit,
        "json_rows": json_rows,
    }
    if min_timestamp:
        params["min_timestamp"] = min_timestamp
    if max_timestamp:
        params["max_timestamp"] = max_timestamp
    if timezone:
        params["timezone"] = timezone

    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "headers": {
                "Authorization": read_token,
            },
        },
        "resource_defaults": {
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "query",
                "endpoint": {
                    "path": "query",
                    "params": params,
                    "data_selector": "rows",
                },
                "primary_key": "span_id",
            },
        ],
    }
    yield from rest_api_resources(config)


def load() -> None:
    read_token = os.getenv("LOGFIRE_READ_TOKEN")
    if not read_token:
        raise RuntimeError(
            "LOGFIRE_READ_TOKEN is missing. Add it to .env before running the pipeline."
        )

    base_url = os.getenv("LOGFIRE_BASE_URL", DEFAULT_BASE_URL)
    sql = os.getenv("LOGFIRE_SQL", DEFAULT_SQL)
    limit = int(os.getenv("LOGFIRE_LIMIT", "1000"))
    json_rows = _env_bool("LOGFIRE_JSON_ROWS", True)
    dataset_name = os.getenv("LOGFIRE_DATASET_NAME", "agent_traces")
    duckdb_path = os.getenv("LOGFIRE_DUCKDB_PATH", "logfire.duckdb")
    min_timestamp = _optional_env("LOGFIRE_MIN_TIMESTAMP")
    max_timestamp = _optional_env("LOGFIRE_MAX_TIMESTAMP")
    timezone = _optional_env("LOGFIRE_TIMEZONE")

    pipeline = dlt.pipeline(
        pipeline_name="logfire_pipeline",
        destination=dlt.destinations.duckdb(duckdb_path),
        dataset_name=dataset_name,
    )
    source = logfire_source(
        read_token=read_token,
        base_url=base_url,
        sql=sql,
        limit=limit,
        json_rows=json_rows,
        min_timestamp=min_timestamp,
        max_timestamp=max_timestamp,
        timezone=timezone,
    )
    load_info = pipeline.run(source)
    print(load_info)


if __name__ == "__main__":
    load()
