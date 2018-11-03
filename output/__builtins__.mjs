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

export function print() {
  var sep = ' ';
  var end = '\n';
  if (arguments.length) {
    var ilastarg = arguments.length - 1;
    if (arguments[ilastarg] &&
                    arguments[ilastarg].hasOwnProperty("__kwargs__")) {
      var allargs = arguments[ilastarg--];
      for (var attrib in allargs) {
        switch (attrib) {
          case 'sep': var sep = allargs[attrib]; break;
          case 'end': var end = allargs[attrib]; break;
        }
      }
    }
    var args = [].slice.apply(arguments).slice(0, ilastarg + 1);
  } else {
    var args = [];
  }
  var string_args = [];
  for (var arg of args) {
    string_args.append(str(arg));
  }
  console.log(sep.join(string_args));
}
