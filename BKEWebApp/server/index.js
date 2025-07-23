const express = require('express');
const cors = require('cors');
const enrichmentRoutes = require('./routes/enrichment');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.use('/api/enrich', enrichmentRoutes);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
