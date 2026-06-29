# test-vuln-repo

Test fixture for the Agentic Dependabot. Every file in this repo exists to
exercise a specific code path in the agent. Do not "clean up" the things that
look weird — they are weird on purpose.

## Coverage matrix

| Vulnerable pkg     | Source uses it?               | Tests pass after bump? | Agent path exercised                                  |
|--------------------|-------------------------------|------------------------|-------------------------------------------------------|
| `requests==2.6.0`  | `app/http_client.py`          | yes                    | scan → bump → run_tests → open_pr                     |
| `urllib3==1.24.0`  | `app/http_client.py`          | yes                    | scan → bump → run_tests → open_pr                     |
| `jinja2==2.10.0`   | `app/render.py`               | yes                    | scan → bump → run_tests → open_pr                     |
| `flask==2.0.0`     | `app/web.py` (broken import!) | **no**                 | scan → bump → run_tests **(fail)** → analyze_failure → edit_code → run_tests → open_pr (or escalate after 3 failed LLM fix attempts) |
| `pytest>=8` (dev)  | implicit (runs the suite)     | depends                | exercises the dev-dep manifest bump path              |

## The Flask trap

`app/web.py` imports `Markup` from `flask`. That symbol was removed in
Flask 2.3 (moved to `markupsafe`). When the agent bumps `flask==2.0.0` to
something ≥ 2.3, the import breaks and the test suite fails. The agent must
notice, run the LLM analyzer, propose a code edit, apply it, and re-run.

Expected successful edit:

```diff
-from flask import Flask, Markup
+from flask import Flask
+from markupsafe import Markup
```

If the LLM/Bedrock credentials are not configured the agent escalates after
`max_iterations` attempts and opens a GitHub issue (or just logs the
escalation if `--github-token` is empty).

## What to look for in the agent run

- A PR for each of `requests`, `urllib3`, `jinja2`, `flask`, `pytest`
- The `flask` PR includes a source-code edit in `app/web.py`
- The `flask` PR commit body lists `Files edited`
- `pytest` PR only touches `requirements-dev.txt`
- `main` is clean at the end with no leftover branches checked out

## Running locally

```bash
# scan only
vuln-agent scan --repo .

# dry-run (no mutations)
vuln-agent run --repo . --dry-run

# full run (needs GITHUB_PAT + GITHUB_REPO; AWS creds for the LLM fix path)
vuln-agent run --repo . --ecosystem pypi
```
