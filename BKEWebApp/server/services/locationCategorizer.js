const knownCities = ['chicago', 'new york', 'boston', 'seattle', 'dallas'];

function getLocation(tokens) {
  const found = tokens.find(token => knownCities.includes(token));
  return found ? capitalize(found) : 'Unknown';
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

module.exports = getLocation;
