import React from 'react';
import TitleResultCard from './TitleResultCard';

function OutputPanel({ results }) {
  return (
    <div>
      <h2>Enriched Results</h2>
      {results.length === 0 ? (
        <p>No results yet.</p>
      ) : (
        results.map((res, index) => (
          <TitleResultCard key={index} data={res} />
        ))
      )}
    </div>
  );
}

export default OutputPanel;
