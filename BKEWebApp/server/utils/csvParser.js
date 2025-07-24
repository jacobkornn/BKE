const csv = require('csv-parser');
const { Readable } = require('stream');

function parseCsvData(csvText) {
  return new Promise((resolve, reject) => {
    const results = [];

    Readable.from(csvText)
      .pipe(csv())
      .on('data', (row) => {
        if (row.jobTitle) results.push(row.jobTitle);
      })
      .on('end', () => resolve(results))
      .on('error', reject);
  });
}

module.exports = parseCsvData;
