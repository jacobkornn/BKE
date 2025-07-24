import React, { useState } from 'react';
import { enrichSingle, enrichBulk } from '../services/api';

function InputPanel({ setResults }) {
  const [text, setText] = useState('');

  const handleTextSubmit = async () => {
    if (!text.trim()) return;
    const result = await enrichSingle(text.trim());
    setResults([result]);
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const text = await file.text();
    let payload = null;

    if (file.name.endsWith('.json')) {
      payload = JSON.parse(text);
    } else if (file.name.endsWith('.csv')) {
      const rows = text.split('\n').filter(Boolean);
      const jobTitles = rows.map(r => r.trim().replace(/^"|"$/g, ''));
      payload = { jobTitles };
    }

    if (payload?.jobTitles?.length) {
      const result = await enrichBulk(payload.jobTitles);
      setResults(result);
    }
  };

  return (
    <div>
      <h3>Enter Job Title</h3>
      <input
        type="text"
        value={text}
        placeholder="e.g. Senior Data Engineer - Seattle"
        onChange={(e) => setText(e.target.value)}
        style={{ width: '100%', marginBottom: '10px' }}
      />
      <button onClick={handleTextSubmit}>Enrich</button>

      <hr />

      <h4>Or Upload JSON/CSV</h4>
      <input type="file" accept=".json,.csv" onChange={handleFileUpload} />
    </div>
  );
}

export default InputPanel;
