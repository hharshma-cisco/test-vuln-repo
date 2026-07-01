# test-repo — end-to-end fixture for Agentic Dependabot

Every file in this repo exists to trigger a specific code path in the
agent. **Do not "clean up" the things that look weird — they are weird
on purpose.**

Companion docs at the project root:

- `EXPECTATIONS.md` — behavior spec for each feature, keyed to code.
- `RUN_PLAYBOOK.md` — step-by-step commands to run against this repo
  with expected output at each step.

---

## Layout

```
test-repo/
├── .vuln-agent.toml               # ignore rules, versioning-strategy, extra_labels
├── .github/workflows/ci.yml       # GHA adapter target
├── services/api/                  # PyPI sub-project (mono-repo path 1)
│   ├── requirements.txt           # 7 vulns of varied shapes
│   ├── app/
│   │   ├── __init__.py
│   │   ├── http_client.py         # safe bump (requests, urllib3)
│   │   ├── render.py              # safe bump (jinja2)
│   │   └── web.py                 # BREAKS on Flask ≥ 2.3 → LLM edit needed
│   └── tests/                     # exercises pytest auto-detection
├── apps/web/                      # npm sub-project (mono-repo path 2)
│   ├── package.json               # direct dep vuln (lodash)
│   ├── package-lock.json          # transitive vuln (qs via express)
│   └── index.test.js              # `npm test` target
└── libs/shared/                   # extra Python manifest → tests monorepo walk
    └── requirements.txt           # pyyaml only, wholly ignored via config
```

---

## Coverage matrix

The purpose of each pin is described. If OSV changes an advisory
between now and when you read this, some rows may drift — that's fine,
the SHAPE of the test (multi-vuln, breaking bump, transitive, etc.)
still holds.

### `services/api/requirements.txt`

| Pin | Why | Expected agent behavior |
|---|---|---|
| `requests==2.6.0` | safe bump | scan → batch → bump → tests pass → PR (`safe-bump`, `conf-very-high`) |
| `urllib3==1.24.0` | safe bump | same batch as `requests`; batch PR bundles both |
| `jinja2==2.10.0` | safe bump | joins the batch |
| `flask==2.0.0` | **breaks on 2.3+** (Markup moved to markupsafe) | forces batch → split fallback, then single-vuln LLM analyze+edit loop |
| `werkzeug==2.0.0` | co-bump candidate with flask | if flask install fails w/ pip conflict, cobump recovery kicks in |
| `pyyaml==5.3` | **[[ignore]]**'d in config | never reaches OSV; watch for `ignoring pyyaml … per [[ignore]] rule` log |
| `django==3.2.0` | governed by `versioning-strategy: patch-only` | OSV safe version is a minor/major bump → **advisory DROPPED** post-scan |

### `apps/web/package.json` + `package-lock.json`

| Pin | Why | Expected agent behavior |
|---|---|---|
| `lodash: 4.17.4` (direct) | direct-dep bump | rewrites `dependencies`, deterministic strategy |
| `express: 4.16.0` (direct) | pulls a vulnerable `qs@6.5.0` transitively | agent scans `qs` via lock file, tags `transitive: True` |
| `qs 6.5.0` (transitive via express) | force the parent-bump path | agent tries `express@<next>` versions smallest-first via `npm view`; if a parent version resolves `qs` to a safe version → `parent_bump` strategy; else `overrides` fallback |

### `.github/workflows/ci.yml`

| `uses:` | Purpose | Expected agent behavior |
|---|---|---|
| `actions/checkout@v3` | any GHA advisory | rewrites `uses:` line, preserves `v` prefix |
| `actions/setup-python@v4` | may or may not have an advisory | if OSV returns nothing, no PR — validates negative case |

### `libs/shared/requirements.txt`

| Pin | Purpose | Expected agent behavior |
|---|---|---|
| `pyyaml==5.3` | second location for a globally-ignored package | proves `[[ignore]]` is repo-wide, not per-manifest |

### `.vuln-agent.toml`

- `excluded_packages = ["some-legacy-cli"]` — legacy field is read (no side effect).
- `[test] timeout = 120` — bumps the pytest timeout override.
- `[pr] extra_labels = ["security", "auto-review"]` — every PR must show these.
- `[[ignore]] package = "pyyaml"` — repo-wide ignore.
- `[[ignore]] package = "requests" versions = ["<2.0"]` — narrow rule that should NOT fire (proves version filtering).
- `[versioning-strategy] "django" = "patch-only"` — drops the django advisory.

---

## Features exercised

- ✅ Multi-manifest monorepo walk (`services/api`, `apps/web`, `libs/shared`)
- ✅ PyPI adapter
- ✅ npm adapter with `package-lock.json` v3
- ✅ npm transitive parent-bump path (express → qs)
- ✅ github-actions adapter
- ✅ `[[ignore]]` rules (both wildcard and version-range)
- ✅ `[versioning-strategy]` patch-only enforcement
- ✅ `[pr] extra_labels`
- ✅ Batch grouping (multiple pypi vulns share a cluster)
- ✅ Batch → split fallback (flask breaks the batch)
- ✅ LLM analyze + edit loop (flask Markup migration)
- ✅ Adversarial edit verification (LLM refuter)
- ✅ Cobump recovery (if flask needs werkzeug bumped for pip to install)
- ✅ Flaky-test retry (needs an actual flake; documented separately)
- ✅ Prompt-injection sanitization (implicit — every LLM call routes untrusted strings)
- ✅ Confidence score in PR body + `conf-*` label
- ✅ Age signal via npm/PyPI registries
- ✅ Release notes via GitHub Releases
- ✅ PR idempotency on re-runs
- ✅ Token budget cap (`--max-tokens`)
- ✅ Offline mode (`--no-llm`)
- ✅ Rollback (`vuln-agent revert`)
- ✅ Run report + explain

---

## What you should NOT expect to see

- **`pyyaml` in scan output** — always filtered by `[[ignore]]`.
- **`django` in PR output** — filtered by `versioning-strategy patch-only`.
- **A `some-legacy-cli` warning** — the excluded-packages field is a no-op here because the package isn't installed anywhere.
