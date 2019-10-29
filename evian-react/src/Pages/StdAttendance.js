import React from "react";
import { connect } from "react-redux";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Divider from "@material-ui/core/Divider";
import { withStyles } from "@material-ui/core/styles";

const styles = theme => ({
  list: {
    padding: "0"
  }
});

function StdAttendance(props) {
  const { classes } = props;

  // vars from store
  const { attendance } = props;
  return (
    <React.Fragment>
      {attendance.length > 0 && (
        <Grid item xs={6}>
          <Paper>
            <List className={classes.list}>
              {attendance.map((att, index) => (
                <React.Fragment key={index}>
                  <ListItem
                    //   button
                    key={index}
                  >
                    <ListItemText
                      primary={`${att.index} | ${att.type} | ${att.date} | ${att.time} | ${att.duration} | ${att.status}`}
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
    attendance: state.PagesReducer.attendance
  };
};

export default connect(
  mapStateToProps,
  null
)(withStyles(styles)(StdAttendance));
