const express = require('express');
const router = express.Router();
const { enrichTitle, enrichTitlesInBulk } = require('../services/enrichmentService');
const csvParser = require('../utils/csvParser');

router.post('/', async (req, res) => {
  const { jobTitle, jobTitles, csvData } = req.body;

  try {
    let result;

    if (jobTitle) {
      result = enrichTitle(jobTitle);
    } else if (jobTitles && Array.isArray(jobTitles)) {
      result = enrichTitlesInBulk(jobTitles);
    } else if (csvData) {
      const titles = await csvParser(csvData); // Convert CSV string to title array
      result = enrichTitlesInBulk(titles);
    } else {
      return res.status(400).json({ error: 'Missing valid input: jobTitle, jobTitles, or csvData' });
    }

    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Enrichment failed', details: err.message });
  }
});

module.exports = router;
