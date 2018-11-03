import {__kwargs__, print} from "./__builtins__.mjs";
import * as functions from "./functions.mjs";
functions.kwargs_with_default('hi', __kwargs__({msg: 'test2'}));
