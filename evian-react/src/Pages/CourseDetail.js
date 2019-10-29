import React from "react";
import { connect } from "react-redux";
import StdAttendance from "./StdAttendance";
import CourseStats from "./CourseStats";
import { STAFF, STUDENT } from "../utils/constants";

function CourseDetail(props) {
  // vars from store
  const { domain } = props;

  if (domain === STUDENT) {
    return <StdAttendance />;
  } else if (domain === STAFF) {
    return <CourseStats />;
  }
}

const mapStateToProps = state => {
  return {
    domain: state.PagesReducer.domain
  };
};

export default connect(
  mapStateToProps,
  null
)(CourseDetail);
