import React from "react";
import { connect } from "react-redux";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";

import Form from "./Form";

const useStyle = makeStyles(theme => ({
  panel: {
    height: "100vh"
  },
  left: {
    backgroundColor: theme.palette.primary.main
  }
}));

function Login(props) {
  
  const classes = useStyle();

  return (
    <Grid container>
      <Grid
        item
        xs={7}
        className={classes.left}
        style={{ height: "100vh" }}
      ></Grid>
      <Grid item xs={5} className={classes.panel}>
        <Grid item xs={12}></Grid>
        <Form {...props} />
      </Grid>
    </Grid>
  );
}

export default connect(
  null,
  null
)(Login);
