import * as actionTypes from "./actionTypes";
import { handleInputUpdate as PagesHandleInputUpdate } from "../../Pages/store/actionCreators";
import { PostLoginAPI } from "../../api";
import { STUDENT, STAFF } from "../../utils/constants";
// import { COURSES } from "../../utils/constants";

export const handleInputUpdate = (name, value) => {
  return {
    type: actionTypes.HANDLE_INPUT_UPDATE,
    name,
    value
  };
};

export const handleLogin = ownProps => {
  return (dispatch, getState) => {
    const state = getState();
    const { username, password } = state.LoginReducer;

    let check = true;

    if (username.length < 1 || password.length < 1) {
      check = false;
      dispatch(handleInputUpdate("message", "Both fields must be filled"));
      dispatch(handleInputUpdate("error", true));
    }

    if (check) {
      dispatch(handleInputUpdate("error", false));
      // uncomment when endpoint is ready
      // PostLoginAPI({ username, password });
        PostLoginAPI({ username, password }).then(res => {
           // console.log(res.image);
           if (res.state){
            dispatch(PagesHandleInputUpdate("courses", res.course));
            dispatch(PagesHandleInputUpdate("domain", res.domain));
            // empty localstorage
            dispatch(PagesHandleInputUpdate("attendance", []));
            dispatch(PagesHandleInputUpdate("labStats", []));
            dispatch(PagesHandleInputUpdate("tutStats", []));
            dispatch(handleInputUpdate("image", res.image));
           } else {
            dispatch(handleInputUpdate("error", true));
            dispatch(handleInputUpdate("message", "Login failed"));
           }
      // dispatch(PagesHandleInputUpdate("courses", COURSES));
      // dispatch(PagesHandleInputUpdate("domain", STUDENT));
      // const res = { domain: STUDENT };
      if (res.domain === STUDENT) {
        ownProps.history.push("/student");
      } else if (res.domain === STAFF) {
        ownProps.history.push("/staff");
      }
        });
    }
  };
};
