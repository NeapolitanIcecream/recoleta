# Redacted production-fleet shape

This example mirrors the topology of the public three-stream fleet without
copying its private paths, operational settings, recipients, or full topic
lists. It is an onboarding example; the
[public fleet](https://neapolitanicecream.github.io/recoleta/) remains the
product proof.

Run commands from this directory so the relative state paths stay contained:

```bash
cd examples/production-fleet
```

Start Huldra in two terminals:

```bash
uv run --project ../.. huldra store init --db .state/huldra.db
uv run --project ../.. huldra daemon \
  --db .state/huldra.db \
  --host 127.0.0.1 \
  --port 8765
```

```bash
uv run --project ../.. huldra worker \
  --db .state/huldra.db \
  --poll-interval-seconds 300
```

Set your model credential in the shell, inspect the plan, then run the latest
closed UTC day:

```bash
export RECOLETA_LLM_API_KEY="replace-me"
uv run --project ../.. recoleta fleet run day \
  --manifest fleet.yaml \
  --dry-run \
  --json
uv run --project ../.. recoleta fleet run day --manifest fleet.yaml
```

Build and serve the aggregate site:

```bash
uv run --project ../.. recoleta fleet site build --manifest fleet.yaml
uv run --project ../.. python -m http.server 8000 --directory site
```

Use a different LiteLLM model identifier or source query if the examples do not
match your provider or research scope. All source and workflow calls in the
actual run can incur provider or network costs.
