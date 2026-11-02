import express from 'express';

// The app is exported without calling listen(): tests start it on a free port.
export const app = express();

// GET /health: the classic "heartbeat" endpoint of a web service.
app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});
