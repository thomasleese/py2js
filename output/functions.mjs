import {__kwargs__, print} from "./__builtins__.mjs";
export function args_with_default(a, b = 'b', c = 'c') {
  if (arguments.length) {
    var ilastarg = arguments.length - 1;
    if (arguments[ilastarg] &&
                    arguments[ilastarg].hasOwnProperty("__kwargs__")) {
      var allargs = arguments[ilastarg--];
      for (var attrib in allargs) {
        switch (attrib) {
          case 'a': var a = allargs[attrib]; break;
          case 'b': var b = allargs[attrib]; break;
          case 'c': var c = allargs[attrib]; break;
        }
      }
    }
  }
  print(a, b, c);
}
args_with_default('a', 'b2');
export function kwargs_with_default(a) {
  var msg = 'test';
  var kwargs = {};
  if (arguments.length) {
    var ilastarg = arguments.length - 1;
    if (arguments[ilastarg] &&
                    arguments[ilastarg].hasOwnProperty("__kwargs__")) {
      var allargs = arguments[ilastarg--];
      for (var attrib in allargs) {
        switch (attrib) {
          case 'a': var a = allargs[attrib]; break;
          case 'msg': var msg = allargs[attrib]; break;
          default: kwargs[attrib] = allargs[attrib];
        }
      }
      delete kwargs.__kwargs__;
    }
  }
  print(a, msg);
}
kwargs_with_default('hi', __kwargs__({msg: 'test2'}));
