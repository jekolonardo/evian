import * as actionTypes from "./actionTypes";
// import {
//   STAFF,
//   STUDENT,
//   COURSES,
//   ATTENDANCE,
//   LAB_STATS,
//   TUT_STATS,
//   SESSION_ATTENDANCE
// } from "../../utils/constants";

const defaultState = {
  courses: [],
  domain: "",
  attendance: [],
  labStats: [],
  tutStats: [],
  sessionAttendance: [],
  openSession: false,
  tableTitle: ""
};

// const defaultState = {
//   courses: COURSES,
//   domain: STAFF,
//   attendance: ATTENDANCE,
//   labStats: LAB_STATS,
//   tutStats: TUT_STATS,
//   sessionAttendance: SESSION_ATTENDANCE,
//   openSession: false,
//   tableTitle: ""
// };

export default (state = defaultState, action) => {
  var stateCopy = JSON.parse(JSON.stringify(state));
  switch (action.type) {
    case actionTypes.HANDLE_INPUT_UPDATE:
      stateCopy[action.name] = action.value;
      // Set to localstorage
      const json = JSON.stringify(stateCopy);
      localStorage.setItem('page_state', json);
      return stateCopy;
    default:
      // Get from localstorage
      try {
        const json = localStorage.getItem('page_state');
        const page_state = JSON.parse(json);
        if (page_state) {
          state = page_state;
        }
      } catch (e) {
        //Do nothing
      }
      return state;
  }
};
