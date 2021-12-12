import React, { Component } from "react";
import { connect } from "react-redux";
import Header from "./Header";
import { set_reduced_urls,
         get_domains 
        } from '../action/actions'
import NotyfyModal from './NotifyModal'



// NOTES
// Use react icons
// https://react-icons.github.io/react-icons


const keyCodeRangeGenerator = (start, end) => {
  const length = end - start;
  return Array.from({ length }, (_, i) => start + i);
}

const specialSymbols = [173, 95, 45]

const keyCodes = keyCodeRangeGenerator(65,90)
                .concat(keyCodeRangeGenerator(48, 57))
                .concat(keyCodeRangeGenerator(97, 122))
                .concat(specialSymbols);

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

    this.setState({ [name]: name === 'url_custom' ? this.symbolBlocker(value) : value})
  }

  componentDidUpdate = (prevProps, prevState) => {
    if (prevProps.network_message !== this.props.network_message && this.props.network_message === 'url_created'){
      this.setState({ url_destination: '', url_custom: ''})
    }
  }

  componentDidMount = () => {
    !this.props.domains ? this.props.get_domains() : null
  }

  symbolBlocker = (e) => {
      let val2 = e.split('')
      let result = ''

      function checkKey(value) {
        for (var i = 0; i < keyCodes.length; i++) {
          if (keyCodes[i] === value) return true;
        }
        return false;
      }

      result = val2.map( e => {

        if (!checkKey(e.charCodeAt(), keyCodes)) {
        return ''    }

      else {
        return e }})
      return result.join('')
    };

  render() {

    const { url_type,
            url_custom,
            domain_id,
            url_destination } = this.state

    const {
          // VARs
          show_notify_modal,
          domains,
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
            { domains && domains.map(e => <option key={e.id} value={e.id}>{e.domain}</option>)}
          </select>
          <br/>

          <h5>Введите URL назначения</h5>

          <b>https://</b> <input
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
                  <span>Допускаются символы a-z, A-Z, 0-9, - и нижнее подчеркивание _</span>
                  <br/>
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
    domains: state.domains
  };
}

// dispatch data
function mapDispatchToProps(dispatch) {
  return {
    set_reduced_urls: (domain_id, url_custom, url_destination) => dispatch(set_reduced_urls(domain_id, url_custom, url_destination)),
    get_domains: () => dispatch(get_domains())
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(UrlsForm);
