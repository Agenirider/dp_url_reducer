import React, { Component } from "react";
import { Link } from "react-router-dom";


// NOTES
// Use react icons
// https://react-icons.github.io/react-icons

class Header extends Component {
  render() {

    const { location } = this.props

    return (
      <React.Fragment>
        <div className="header">
          <div className="header-title">
              DP URL Reducer
          </div>

          <div className="header-navbar">
              <div className={ location === 'urlform' ? "header-btn" : "header-btn-inactive"}>
                    <Link to='/'>Список</Link>
              </div>
              <div className={ location === 'mainpage' ? "header-btn" : "header-btn-inactive"}>
                    <Link to='/add'>Добавить</Link>
              </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}


export default Header;
