import React from "react";
import Facial from "./Facial";
import Login from "./Login";
import Pages from "./Pages";
import { Route, BrowserRouter } from "react-router-dom";
import { CssBaseline } from "@material-ui/core";
import { connect } from "react-redux";

function App() {
  return (
    <React.Fragment>
      <CssBaseline />
      <BrowserRouter>
        <Route exact path="/" component={Login} />
        <Route exact path="/facial" component={Facial} />
        <Route exact path="/student" component={Pages} />
        <Route exact path="/staff" component={Pages} />
      </BrowserRouter>
    </React.Fragment>
  );
}

export default connect(
  null,
  null
)(App);
