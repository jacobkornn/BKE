const BASE_URL = 'http://localhost:5000/api/enrich';

export async function enrichSingle(jobTitle) {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ jobTitle })
  });
  return await res.json();
}

export async function enrichBulk(jobTitles) {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ jobTitles })
  });
  return await res.json();
}
