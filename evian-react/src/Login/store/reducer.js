import * as actionTypes from "./actionTypes";

const defaultState = {
  username: "",//heng0181
  password: "",
  message: "",
  error: false,
  image: "",
};

export default (state = defaultState, action) => {
  var stateCopy = JSON.parse(JSON.stringify(state));
  switch (action.type) {
    case actionTypes.HANDLE_INPUT_UPDATE:
      stateCopy[action.name] = action.value;
      // set to localstorage
      const json = JSON.stringify(stateCopy);
      localStorage.setItem('login_state', json);
      return stateCopy;
    default:
      // get from localstorage
      try {
        const json = localStorage.getItem('login_state');
        const login_state = JSON.parse(json);
        if (login_state) {
          state = login_state;
        }
      } catch (e) {
        //Do nothing
      }
      return state;
  }
};