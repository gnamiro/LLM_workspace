# Homework: dlt

In this homework we will take the FAQ agent from Module 1,
instrument it with [Pydantic Logfire](https://logfire.dev) for
observability,
then pull the trace data back out with dlt and analyze it.

## Question 1. Instrument the agent with Logfire

Sign up for a free [Logfire](https://logfire.dev) account, create a
project, and generate a write token. Put it in `.env` as
`LOGFIRE_TOKEN`.

Instrument the agent:

```python
logfire.configure()
logfire.instrument_pydantic_ai()
```

Run the agent a few times with different questions and open your
project on Logfire to see the traces.

For the following query

> How do I run Ollama locally?

how many spans does a single agent run produce?

Each span is either the agent run itself, an LLM call, or a tool call.
The number can vary between runs because the model decides how many
times to search.

[ ] 1
[X] 5
[ ] 15
[ ] 30

> Ans: 5

## Question 2. Load traces into DuckDB with dlt

Generate a read token for your Logfire project and set it as
`LOGFIRE_READ_TOKEN` in `.env`.

Initialize a dlt-hub project like in the workshop. Then ask your coding
agent to pull the data from Pydantic Logfire and save it into DuckDB.

The dltHub AI workbench has a ready-made context for Logfire. Point your
agent to it: https://dlthub.com/context/source/logfire

If you don't currently use a coding agent, you can use something like OpenCode:
you should be able to complete one session with the free account.

Alternatively, you can do it in the old way (using ChatGPT or your favorite search engine).


The logfire traces contain deeply nested JSON (span attributes with
LLM messages, tool calls, token usage, etc.). dlt automatically
normalizes this into a set of tables - one for the main records, plus
child tables for each nested level.

How many tables did dlt create? Check with:

```sql
SELECT COUNT(*) FROM information_schema.tables 
WHERE table_schema = 'agent_traces';
```

[ ] 1
[ ] 3
[X] 24
[] 100

> Ans: 24
> Exp: Run logfire_pipeline.py and then count_tables.py and you will see the results.

## Question 3. Query traces with an agent

Using a coding agent (you can also write the code by hand) find the
input token usage for the agent run from Q1.

The token counts are stored in the span attributes as
`gen_ai.usage.input_tokens`. Sum them across all LLM calls within the
trace. The number depends on how many searches the agent made, so
report the range it falls into:

[ ] 100 - 500
[X] 1500 - 5000
[ ] 10000 - 20000
[ ] 50000 - 100000

> Ans: 3563
> Exp: Run the input_toknes.py to get the results
> Note: I noticed that the span_count here shows less spans than the total spans and 
> the justification I could find for this is input tokens shows only the LLM spans not the 
> total spans.

## Submit the results

* Submit your results here: https://courses.datatalks.club/llm-zoomcamp-2026/homework/dlt



# My notes:

- Trace: a trace is the whole request from start to finish
- Span: a span is one step inside that request

> a span is basically a named operation with a start time and end time and with a duration and often metadata like inputs, outputs, tokens, errors, or parent/child relationships!
