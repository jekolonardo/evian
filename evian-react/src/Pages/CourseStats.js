import React from "react";
import { connect } from "react-redux";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Divider from "@material-ui/core/Divider";
import { withStyles } from "@material-ui/core/styles";

import { actionCreators } from "./store";

const styles = theme => ({
  list: {
    padding: "0"
  }
});

function CourseStats(props) {
  const { classes } = props;
  // vars from store
  const { labStats, tutStats } = props;

  // methods from store
  const { loadSessionAttendance, handleInputUpdate } = props;

  return (
    <React.Fragment>
      {labStats.length > 0 && (
        <Grid item xs={3}>
          <Paper>
            <List className={classes.list}>
              {labStats.map((att, index) => (
                <React.Fragment key={index}>
                  <ListItem
                    button
                    key={index}
                    onClick={() => {
                      const title = `${att.course_code} - ${att.index} - ${att.date}`;
                      loadSessionAttendance(att.index, att.date);
                      handleInputUpdate("tableTitle", title);
                    }}
                  >
                    <ListItemText
                      primary={`${att.index} | ${att.date} | ${att.rate}`}
                    />
                  </ListItem>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>
      )}
      {tutStats.length > 0 && (
        <Grid item xs={3}>
          <Paper>
            <List className={classes.list}>
              {tutStats.map((att, index) => (
                <React.Fragment key={index}>
                  <ListItem
                    button
                    key={index}
                    onClick={() => {
                      const title = `${att.course_code} - ${att.index} - ${att.date}`;
                      loadSessionAttendance(att.index, att.date);
                      handleInputUpdate("tableTitle", title);
                    }}
                  >
                    <ListItemText
                      primary={`${att.index} | ${att.date} | ${att.rate}`}
                    />
                  </ListItem>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>
      )}
    </React.Fragment>
  );
}

const mapStateToProps = state => {
  return {
    labStats: state.PagesReducer.labStats,
    tutStats: state.PagesReducer.tutStats
  };
};

const mapDispatchToProps = dispatch => ({
  handleInputUpdate: (name, value) => {
    dispatch(actionCreators.handleInputUpdate(name, value));
  },
  loadSessionAttendance: (index, date) => {
    dispatch(actionCreators.loadSessionAttendance(index, date));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withStyles(styles)(CourseStats));
