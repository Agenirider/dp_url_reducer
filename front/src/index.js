import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import reduxThunk from 'redux-thunk';
import { composeWithDevTools } from 'redux-devtools-extension';
import { Router } from 'react-router-dom';
import { createBrowserHistory } from 'history'

import mainStore from "./components/store";

const devTools =
  process.env.NODE_ENV === "production"
        ? applyMiddleware(reduxThunk)
        : composeWithDevTools(applyMiddleware(reduxThunk));

const store = createStore(
  mainStore,
  devTools
);

const history = createBrowserHistory()

ReactDOM.render(
  <Router history={history}>
    <Provider store={store}>
      <App />
    </Provider>
  </Router>,
  document.getElementById("root")
);
