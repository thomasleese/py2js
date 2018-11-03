String.prototype.join = function(strings) {
  strings = Array.from(strings);
  return strings.join(this);
};
