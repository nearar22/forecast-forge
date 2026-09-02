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
- Contract: [`0x92993B6F786BdE15e62DFD3669f2822A45B3d11f`](https://explorer-studio.genlayer.com/address/0x92993B6F786BdE15e62DFD3669f2822A45B3d11f)
- Deployment transaction: [`0xcf7e075feb378e15c86ccf8dec5f70215ffd9924795b89bced144121c3df4b68`](https://explorer-studio.genlayer.com/tx/0xcf7e075feb378e15c86ccf8dec5f70215ffd9924795b89bced144121c3df4b68)

## Interface

The interface is a living research terminal rather than a betting product: dark data surfaces, monospace metrics, heartbeat network state, count-up values, and slow evidence-phase sweeps. Every animation respects reduced-motion preferences.

ForecastForge is an information and reputation protocol. It does not custody stakes, promise returns, or provide financial advice.

MIT licensed.
