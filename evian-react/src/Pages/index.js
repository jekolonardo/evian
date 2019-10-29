import React from "react";
import { connect } from "react-redux";
import Header from "../Header";
import UserHeader from "./UserHeader";
import CourseList from "./CourseList";
import SessionAttendance from "./SessionAttendance";

function Staff(props) {
  return (
    <React.Fragment>
      <Header />
      <UserHeader />
      <CourseList />
      <SessionAttendance />
    </React.Fragment>
  );
}

export default connect(
  null,
  null
)(Staff);
