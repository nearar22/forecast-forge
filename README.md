# ForecastForge

> A live research terminal for sealed forecasts, timestamped evidence, validator consensus, and portable accuracy.

ForecastForge separates prediction from hindsight. A creator publishes a precise question, explicit outcomes, resolution criteria, and a minimum evidence threshold. Each participant submits one SHA-256 commitment per market, then reveals the outcome, confidence, and nonce only after commitments close. Anyone may contribute an HTTPS evidence snapshot with its content hash, retrieval time, and optional archive URL.

GenLayer validators independently fetch the submitted sources and apply the published criteria to their rendered text. Consensus requires the exact outcome and the same canonical confidence band. Weak, changed, inaccessible, or contradictory evidence produces `UNRESOLVED`, which remains neutral for every forecaster. One evidence-based appeal may recompute the resolution before finalization. Resolved markets update a public, portable accuracy profile on-chain.

## Why GenLayer

Ordinary contracts can count votes but cannot determine whether changing web evidence satisfies a precise real-world condition. ForecastForge uses GenLayer for bounded semantic judgment while deterministic code controls commitments, reveals, evidence integrity, appeal count, finalization, and reputation accounting.

## Integrity model

- One commitment per wallet per market; outcomes and confidence stay sealed until reveal.
- Reveals must reproduce `SHA256(marketId:outcome:confidence:nonce)`.
- Evidence requires a public HTTPS source, SHA-256 of normalized rendered text, and retrieval timestamp.
- Validators fetch every source themselves and reject a snapshot when its submitted hash no longer matches the rendered text.
- Duplicate hashes and duplicate source hosts are rejected; at least two distinct valid source hosts are required.
- Validators must agree on the exact outcome and exact canonical confidence band.
- Prompt text and fetched pages are explicitly treated as untrusted data.
- One appeal per market; the appeal re-runs the same published criteria.
- Any wallet may advance a phase after its recorded deadline, so the creator cannot stall resolution.
- The interface refreshes authoritative state only after `FINALIZED`; accepted and failed transactions remain visibly pending or failed.
- Reveal data is restored locally and can be exported or imported as a recovery file before reveal.
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

Tests cover malformed markets, duplicate wallets, sealed-state privacy, commitment mismatch, source-host independence, fetched-content hash mismatch, permissionless phase progression, consensus resolution, portable accuracy, neutral unresolved markets, and one-appeal enforcement. Frontend tests also cover transaction finality, timeout failure, and reveal recovery.

## Deployment

- Live interface: [forecast-forge-5wy.pages.dev](https://forecast-forge-5wy.pages.dev/)
- Network: GenLayer StudioNet (`61999`)
- Contract: [`0xD19300b8315Ff137c26881F396a564a4Cc96A425`](https://explorer-studio.genlayer.com/address/0xD19300b8315Ff137c26881F396a564a4Cc96A425)
- Deployment transaction: [`0xc251359853dc94999c53034527517a90f24f3abb343d906a91700c61d8b29a7d`](https://explorer-studio.genlayer.com/tx/0xc251359853dc94999c53034527517a90f24f3abb343d906a91700c61d8b29a7d)
- Live market transaction: [`0x738c714bbede77f13905c0e539e7753af3b90e74b9456bbc246600a6cc4c879a`](https://explorer-studio.genlayer.com/tx/0x738c714bbede77f13905c0e539e7753af3b90e74b9456bbc246600a6cc4c879a)

## Interface

The interface is a living research terminal rather than a betting product: dark data surfaces, monospace metrics, heartbeat network state, count-up values, and slow evidence-phase sweeps. Every animation respects reduced-motion preferences.

ForecastForge is an information and reputation protocol. It does not custody stakes, promise returns, or provide financial advice.

MIT licensed.
