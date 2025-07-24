function getOccupation(tokens) {
  if (tokens.includes('engineer')) return 'Software Engineer';
  if (tokens.includes('manager')) return 'Project Manager';
  if (tokens.includes('analyst')) return 'Data Analyst';
  return 'Unknown Occupation';
}

module.exports = getOccupation;
