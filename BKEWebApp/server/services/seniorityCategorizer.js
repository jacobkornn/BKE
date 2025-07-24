function getSeniority(tokens) {
  if (tokens.includes('senior')) return 'Senior';
  if (tokens.includes('lead')) return 'Lead';
  if (tokens.includes('intern')) return 'Intern';
  if (tokens.includes('junior')) return 'Junior';
  return 'Entry-Level';
}

module.exports = getSeniority;
