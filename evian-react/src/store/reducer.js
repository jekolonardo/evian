import { combineReducers } from "redux";

import { reducer as LoginReducer } from "../Login/store";
import { reducer as PagesReducer } from "../Pages/store";

const reducer = combineReducers({
  LoginReducer,
  PagesReducer
});

export default reducer;
