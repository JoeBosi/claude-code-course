import test from 'node:test';
import assert from 'node:assert/strict';
import { app } from './server.js';

test('GET /health returns 200 and status ok', async () => {
  const server = app.listen(0); // port 0 = let the system pick a free port
  const { port } = server.address();
  const res = await fetch(`http://127.0.0.1:${port}/health`);
  const body = await res.json();
  server.close();
  assert.equal(res.status, 200);
  assert.equal(body.status, 'ok');
});
