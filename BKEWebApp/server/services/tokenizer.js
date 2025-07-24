function tokenize(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s]/g, '') // remove punctuation
    .split(/\s+/)
    .filter(Boolean);
}

module.exports = tokenize;
