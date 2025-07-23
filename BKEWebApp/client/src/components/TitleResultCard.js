import React from 'react';

function TitleResultCard({ data }) {
  return (
    <div style={{ marginBottom: '15px', padding: '10px', border: '1px solid #ccc' }}>
      <strong>{data.inputTitle}</strong>
      <ul>
        <li><strong>Occupation:</strong> {data.occupation}</li>
        <li><strong>Function:</strong> {data.function}</li>
        <li><strong>Seniority:</strong> {data.seniority}</li>
        <li><strong>Location:</strong> {data.location}</li>
      </ul>
    </div>
  );
}

export default TitleResultCard;
