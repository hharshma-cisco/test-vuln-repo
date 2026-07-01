// Minimal test so `npm test` returns 0 for a clean bump. The agent
// probes tests to decide whether a bump is safe-bump or needs the LLM
// edit path. lodash/express bumps DON'T break anything the agent can
// observe here, so this stays green.
const test = require('node:test');
const assert = require('node:assert');

test('sanity', () => {
  assert.strictEqual(1 + 1, 2);
});
