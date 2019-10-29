import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Avatar from "@material-ui/core/Avatar";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import avatar from "../static/images/avatar/avatar.jpg";
import { handleLogout } from "./store/actionCreators";

const useStyle = makeStyles(theme => ({
  avatar: {
    margin: theme.spacing(2),
    width: 60,
    height: 60
  }
}));

function UserHeader(props) {
  const classes = useStyle();

  // vars from login store
  const { username , image } = props;

  // method from page store
  const { handleLogout } = props

  var base64Icon = avatar;
  if (image !== ""){
    base64Icon = 'data:image/jpg;base64,'+image;
  }

  return (
    <Container maxWidth="lg">
      <Paper>
        <Grid container justify="center" alignItems="center">
          <Grid item xs={5}>
            <Avatar alt="avatar" src={base64Icon} className={classes.avatar} />
          </Grid>
          <Grid item xs={5}>
            <Typography variant="h6">{username}</Typography>
          </Grid>
          <Grid item xs={2}>
            <Link to="/">
              <Button
                variant="contained"
                color="secondary"
                onClick={() => handleLogout()}>
                Logout
              </Button>
            </Link>
        </Grid>
        </Grid>
      </Paper>
    </Container>
  );
}

const mapStateToProps = state => {
  return {
    username: state.LoginReducer.username,
    image: state.LoginReducer.image
  };
};

const mapDispatchToProps = (dispatch) => ({
  handleLogout: () => {
    dispatch(handleLogout());
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(UserHeader);
