function getFunction(tokens) {
  if (tokens.includes('cloud')) return 'Engineering > Cloud';
  if (tokens.includes('data')) return 'Analytics > Data';
  if (tokens.includes('marketing')) return 'Marketing > General';
  return 'General Function';
}

module.exports = getFunction;
