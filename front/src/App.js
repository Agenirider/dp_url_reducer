import React, { Component } from "react";
import MainPage from "./components/main/MainPage";
import UrlsForm from "./components/main/UrlsForm";
import "./components/index.css";
import { Switch, Route } from "react-router";
import { Router } from "react-router-dom";
import { createBrowserHistory } from "history";

class App extends Component {
  render() {
    const customHistory = createBrowserHistory();

    const Main = () => (
      <Router history={customHistory}>
        <Switch>
          <Route exact  path="/" component={ MainPage } />
          <Route exact  path="/add" component={ UrlsForm } />
        </Switch>
      </Router>
    );

    return (
      <React.Fragment>
        <Main />
      </React.Fragment>
    );
  }
}



export default App;
