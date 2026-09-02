# ForecastForge

> A live research terminal for sealed forecasts, timestamped evidence, validator consensus, and portable accuracy.

ForecastForge separates prediction from hindsight. A creator publishes a precise question, explicit outcomes, resolution criteria, and a minimum evidence threshold. Each participant submits one SHA-256 commitment per market, then reveals the outcome, confidence, and nonce only after commitments close. Anyone may contribute an HTTPS evidence snapshot with its content hash, retrieval time, and optional archive URL.

GenLayer validators apply the published criteria to at least two snapshots. Consensus requires the same outcome and confidence within 10 points. Weak or contradictory evidence produces `UNRESOLVED`, which remains neutral for every forecaster. One evidence-based appeal may recompute the resolution before finalization. Resolved markets update a public, portable accuracy profile on-chain.

## Why GenLayer

Ordinary contracts can count votes but cannot determine whether changing web evidence satisfies a precise real-world condition. ForecastForge uses GenLayer for bounded semantic judgment while deterministic code controls commitments, reveals, evidence integrity, appeal count, finalization, and reputation accounting.

## Integrity model

- One commitment per wallet per market; outcomes and confidence stay sealed until reveal.
- Reveals must reproduce `SHA256(marketId:outcome:confidence:nonce)`.
- Evidence requires HTTPS, a SHA-256 content snapshot, and retrieval timestamp.
- Duplicate snapshots are rejected; archive URLs preserve mutable sources when available.
- At least two independent snapshots are required before resolution.
- Validators must agree on the exact outcome and confidence within a 10-point tolerance.
- Prompt text and fetched pages are explicitly treated as untrusted data.
- One appeal per market; the appeal re-runs the same published criteria.
- `UNRESOLVED` never counts as correct or incorrect.
- `get_profile(address)` exposes resolved, correct, incorrect, and accuracy values to other applications.

## Lifecycle

`COMMIT` → `REVEAL` → `EVIDENCE` → `APPEAL` → `FINAL`

## Verification

```bash
gltest tests -v
cd frontend
npm test
npm run build
```

Tests cover malformed markets, duplicate wallets, sealed-state privacy, commitment mismatch, invalid evidence snapshots, consensus resolution, portable accuracy, neutral unresolved markets, and one-appeal enforcement.

## Deployment

- Live interface: [forecast-forge-5wy.pages.dev](https://forecast-forge-5wy.pages.dev/)
- Network: GenLayer StudioNet (`61999`)
- Contract: [`0x89933004dAbBa1C5080838485aeFd0651AC9327C`](https://explorer-studio.genlayer.com/address/0x89933004dAbBa1C5080838485aeFd0651AC9327C)
- Deployment transaction: [`0xff1a17c4e06e576c94146da591c88f00a5f323eb482e6b167f9cb6cabe3999e3`](https://explorer-studio.genlayer.com/tx/0xff1a17c4e06e576c94146da591c88f00a5f323eb482e6b167f9cb6cabe3999e3)
- Live market transaction: [`0x6ae2090d3b1f3d4caa735fc9403b6d834aa9aa21408d165b689926157c902007`](https://explorer-studio.genlayer.com/tx/0x6ae2090d3b1f3d4caa735fc9403b6d834aa9aa21408d165b689926157c902007)

## Interface

The interface is a living research terminal rather than a betting product: dark data surfaces, monospace metrics, heartbeat network state, count-up values, and slow evidence-phase sweeps. Every animation respects reduced-motion preferences.

ForecastForge is an information and reputation protocol. It does not custody stakes, promise returns, or provide financial advice.

MIT licensed.
