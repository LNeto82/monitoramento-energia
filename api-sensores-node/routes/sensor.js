const express = require('express');
const router = express.Router();
const axios = require('axios');
const { createClient } = require('redis');

const redisClient = createClient();
redisClient.connect();

// GET /sensor-data
router.get('/sensor-data', async (req, res) => {
  const cache = await redisClient.get('sensorData');
  if (cache) return res.json(JSON.parse(cache));

  const data = {
    temperature: (Math.random() * 100).toFixed(2),
    pressure: (Math.random() * 100).toFixed(2)
  };

  await redisClient.set('sensorData', JSON.stringify(data), { EX: 30 });
  res.json(data);
});

// POST /alert
router.post('/alert', async (req, res) => {
  try {
    await axios.post('http://localhost:5002/event', req.body);
    res.status(200).send('Alerta enviado');
  } catch (err) {
    res.status(500).send('Erro ao enviar alerta');
  }
});

module.exports = router;
