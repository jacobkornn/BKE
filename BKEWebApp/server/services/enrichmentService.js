const tokenize = require('./tokenizer');
const resolveTokens = require('./resolver');
const getOccupation = require('./occupationCategorizer');
const getFunction = require('./functionCategorizer');
const getSeniority = require('./seniorityCategorizer');
const getLocation = require('./locationCategorizer');

function enrichTitle(jobTitle) {
  const tokens = tokenize(jobTitle);
  const resolved = resolveTokens(tokens);

  return {
    inputTitle: jobTitle,
    occupation: getOccupation(resolved),
    function: getFunction(resolved),
    seniority: getSeniority(resolved),
    location: getLocation(resolved)
  };
}

function enrichTitlesInBulk(titles = []) {
  return titles.map(title => enrichTitle(title));
}

module.exports = { enrichTitle, enrichTitlesInBulk };
