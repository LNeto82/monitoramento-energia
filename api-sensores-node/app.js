const express = require('express');
const sensorRoutes = require('./routes/sensor');

const app = express();
app.use(express.json());
app.use('/', sensorRoutes);

app.listen(4001, () => {
  console.log('Sensor API rodando na porta 4001');
});
