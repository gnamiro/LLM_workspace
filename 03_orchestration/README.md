# Module 3: AI Orchestration with Kestra

## Question 1: Context Engineering
Try the following experiment:

1. Open ChatGPT in a private browser window: https://chatgpt.com 
2. Enter this prompt: "Create a Kestra flow that loads NYC taxi data from CSV to BigQuery"
3. Then, use Kestra's AI Copilot with the same prompt

After trying the same prompt in ChatGPT vs Kestra's AI Copilot, what is the primary reason AI Copilot generates better Kestra flows?

- [ ] AI Copilot uses a more powerful model
- [x] AI Copilot has access to current Kestra plugin documentation
- [ ] AI Copilot uses more tokens
- [ ] AI Copilot has internet access

## Question 2: RAG vs No RAG
Run both `1_chat_without_rag.yaml` and `2_chat_with_rag.yaml` in the Kestra UI. Read the execution logs for each.

The non-RAG response about Kestra 1.1 features is best described as:

- [ ] Accurate and specific, matching the actual release notes
- [x] Vague, generic, or fabricated — the model guesses from training data
- [ ] Empty — the model refuses to answer without context
- [ ] Identical to the RAG version

## Question 3: Token usage — short summary
Run `4_simple_agent.yaml` with `summary_length = short` (leave the other inputs as defaults).

Open the execution logs and find the token usage logged by the `log_token_usage` task.

What is the approximate output token count for `multilingual_agent`?

- [ ] 5-15 tokens
- [x] 60-100 tokens
- [ ] 200-400 tokens
- [ ] 500+ tokens

> output token: 72

## Question 4: Token usage — long summary
Run `4_simple_agent.yaml` with `summary_length = long`.

Compare the `multilingual_agent` output token count to your result from Question 3. Roughly how many times more output tokens does the long summary use?

- [ ] About the same (within 20%)
- [x] 2-5x more
- [ ] 10-20x more
- [ ] 50x more

> output token: 170

## Question 5: Modifying a flow
Open `4_simple_agent.yaml` in the Kestra flow editor. Find the `english_brevity` task and change its prompt from asking for exactly 1 sentence to asking for exactly 3 sentences.

Save the flow, then run it with `summary_length = long`.

Compare the `english_brevity` output token count to the original 1-sentence version (also with `summary_length = long`). How do they compare?

- [ ] About the same (within 20%)
- [x] 2-4x more
- [ ] 5-10x more
- [ ] 10x+ more

> Token usage with exactly 1-sentence and long summary-length: 60
> Token usage with exactly 3-sentence and long summary-length: 92
> The comparison: 92/60 = 1.53

## Question 6: Best Practices
Based on what you learned in this module, for production workflows requiring deterministic, repeatable results with strict compliance requirements (e.g., financial reporting, workflows in highly regulated industries), which approach is most appropriate?

- [ ] Always use AI agents for maximum flexibility and adaptation
- [x] Use traditional task-based workflows for predictability and auditability
- [ ] Use only RAG without agents for better performance
- [ ] Use web search tools exclusively to ensure current data