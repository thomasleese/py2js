export function __kwargs__(object) {
  object.__kwargs__ = true;
  return object;
}

export function str(stringable) {
  if (typeof stringable === 'number') {
    return stringable.toString();
  } else {
    try {
      return stringable.__str__();
    } catch (exception) {
      try {
        return repr(stringable);
      } catch (exception) {
        return String(stringable);
      }
    }
  }
}

String.prototype.join = function(strings) {
  strings = Array.from(strings);
  return strings.join(this);
};

Array.prototype.append = function(element) {
  this.push(element);
};
