import React from "react";
import { connect } from "react-redux";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { withStyles } from "@material-ui/core/styles";

import CourseDetail from "./CourseDetail";

import { actionCreators } from "./store";
import { STUDENT } from "../utils/constants";

const styles = theme => ({
  root: {
    marginTop: theme.spacing(4)
  },
  list: {
    padding: "0"
  }
});

function StdCourseList(props) {
  const { classes } = props;

  // vars from store
  const { courses, domain } = props;

  // methods from store
  const { loadAttendance } = props;
  return (
    <React.Fragment>
      <Container maxWidth="lg" className={classes.root}>
        <Grid container spacing={1}>
          <Grid item xs={6}>
            <Paper>
              <List className={classes.list}>
                {courses.map(course => (
                  <ListItem
                    button
                    key={course.code}
                    onClick={() => loadAttendance(course.name)}
                  >
                    {domain === STUDENT ? (
                      <ListItemText
                        primary={`${course.name} - ${course.code} - ${course.group}`}
                      />
                    ) : (
                      <ListItemText
                        primary={`${course.name} - ${course.code} `}
                      />
                    )}
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
          <CourseDetail />
        </Grid>
      </Container>
    </React.Fragment>
  );
}

const mapStateToProps = state => {
  return {
    courses: state.PagesReducer.courses,
    domain: state.PagesReducer.domain
  };
};

const mapDispatchToProps = dispatch => ({
  loadAttendance: course => {
    dispatch(actionCreators.loadAttendance(course));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withStyles(styles)(StdCourseList));
