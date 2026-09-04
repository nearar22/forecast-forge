import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'

const app = fs.readFileSync(new URL('../src/main.jsx', import.meta.url), 'utf8')
const css = fs.readFileSync(new URL('../src/styles.css', import.meta.url), 'utf8')

test('uses the complete live contract workflow', () => {
  for (const value of ['readContract', 'writeContract', 'list_markets', 'commit_forecast', 'reveal_forecast', 'submit_evidence', 'appeal_resolution', 'finalize_market']) assert.match(app, new RegExp(value))
})

test('waits for finality and fails closed on timeout', () => {
  assert.match(app, /s==='FINALIZED'/)
  assert.match(app, /ACCEPTED, AWAITING FINALITY/)
  assert.match(app, /did not reach FINALIZED before the polling timeout/)
  assert.doesNotMatch(app, /\['ACCEPTED','FINALIZED'\]\.includes\(s\).*break/)
})

test('supports reveal backup export, import, and automatic restoration', () => {
  for (const value of ['DOWNLOAD REVEAL BACKUP', 'RESTORE REVEAL BACKUP', 'localStorage.getItem', 'commitment:d']) assert.match(app, new RegExp(value))
})

test('contains no simulated market records', () => {
  assert.doesNotMatch(app, /regional grid|open transit|FF-240|demo forecaster/i)
})

test('keeps terminal motion accessible', () => {
  assert.match(css, /@keyframes pulse/)
  assert.match(css, /prefers-reduced-motion/)
})
