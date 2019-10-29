import React from "react";
import { connect } from "react-redux";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";

import Message from "../Message";

import { actionCreators } from "./store";

const useStyle = makeStyles(theme => ({
  form: {
    marginTop: theme.spacing(10),
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
    paddingBottom: theme.spacing(4),
    paddingTop: theme.spacing(4)
  },
  msg: {
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2)
  }
}));

function Form(props) {
  
  const classes = useStyle();

  //   vars from store
  const { username, password, message, error } = props;

  //   methods from store
  const { handleInputUpdate, handleLogin } = props;

  return (
    <Paper className={classes.form}>
      <Grid
        container
        spacing={4}
        justify="center"
        alignContent="center"
        alignItems="center"
      >
        <Grid item xs={12}>
          <Message
            className={classes.msg}
            variant="error"
            message={message}
            open={error}
            onClose={() => handleInputUpdate("error", false)}
          />
        </Grid>
        <Grid item xs={12}>
          <Typography variant="h5" color="primary" align="center">
            LOGIN
          </Typography>
        </Grid>
        <Grid item xs={10}>
          <TextField
            fullWidth
            label="Username"
            value={username}
            name="username"
            onChange={e => handleInputUpdate(e.target.name, e.target.value)}
          />
        </Grid>
        <Grid item xs={10}>
          <TextField
            fullWidth
            label="Password"
            type="password"
            value={password}
            name="password"
            onChange={e => handleInputUpdate(e.target.name, e.target.value)}
          />
        </Grid>
        <Grid item xs={10}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={() => handleLogin()}
          >
            Login
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
}

const mapStateToProps = state => {
  return {
    username: state.LoginReducer.username,
    password: state.LoginReducer.password,
    message: state.LoginReducer.message,
    error: state.LoginReducer.error
  };
};

const mapDispatchToProps = (dispatch, ownProps) => ({
  handleInputUpdate: (name, value) => {
    dispatch(actionCreators.handleInputUpdate(name, value));
  },
  handleLogin: () => {
    dispatch(actionCreators.handleLogin(ownProps));
  }
});
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Form);
