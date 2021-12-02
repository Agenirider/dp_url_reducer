import React, { Component } from "react";
import { connect } from "react-redux";
import Header from "./Header";
import { set_reduced_urls } from '../action/actions'
import NotyfyModal from './NotifyModal'



// NOTES
// Use react icons
// https://react-icons.github.io/react-icons

class UrlsForm extends Component {

  state = {
    url_type: 'generate', // OR custom
    url_custom: '',
    domain_id: 1,
    url_destination: '',
  }

  handleInputChange = (event) => {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    this.setState({ [name]: value})
  }

  componentDidUpdate = (prevProps, prevState) => {
    if (prevProps.network_message !== this.props.network_message && this.props.network_message === 'url_created'){
      this.setState({ url_destination: '', url_custom: ''})
    }
  }


  render() {

    const { url_type,
            url_custom,
            domain_id,
            url_destination } = this.state

    const {
          // VARs
          show_notify_modal,
          // FUNC
          set_reduced_urls } = this.props


    return (
    <React.Fragment>

        <Header location={'urlform'}/>

        { show_notify_modal ? <NotyfyModal/> : null}


        <div className='dp-test-url-container'>
        <h5>Выберите домен</h5>
          <select value={ domain_id }
              name="domain_id"
              onChange={this.handleInputChange}
              >
            <option value='1'>domain1.link</option>
            <option value='2'>dom123.com</option>
            <option value='3'>test123.ru</option>
            <option value='4'>lalala.we</option>
            <option value='blablabla.com'>blablabla.com</option>
          </select>
          <br/>

          <h5>Введите URL назначения</h5>

          <input
            type="text"
            name="url_destination"
            maxLength="500"
            onChange={this.handleInputChange}
            value={ url_destination }
            />
          <br/>

          <h5>Выберите тип URL</h5>
          <select value={ url_type }
              name="url_type"
              onChange={this.handleInputChange}
              >
              <option value='generate'>Сгенерировать автоматически</option>
              <option value='custom'>Задать вручную</option>
          </select>
          <br/>

          { url_type === 'custom'
              ? (<React.Fragment>
                  <h5>Введите URL</h5>
                  <input
                    type="text"
                    name="url_custom"
                    maxLength="200"
                    onChange={this.handleInputChange}
                    value={ url_custom }
                    />
                </React.Fragment>)
              : null
            }
            <br/>
            <hr/>
            <div className= 'db-test-btn-active'
                className={ url_destination !== '' ? 'db-test-btn-active' : 'db-test-btn-inactive'}
                onClick={() => { url_destination !== '' && set_reduced_urls(domain_id, url_custom, url_destination) } }>Отправить</div>
            </div>

    </React.Fragment>)
  }
}



// connect state
function mapStateToProps(state) {
  return {
    show_notify_modal: state.show_notify_modal,
    network_message: state.network_message,
  };
}

// dispatch data
function mapDispatchToProps(dispatch) {
  return {
    set_reduced_urls: (domain_id, url_custom, url_destination) => dispatch(set_reduced_urls(domain_id, url_custom, url_destination))
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(UrlsForm);
