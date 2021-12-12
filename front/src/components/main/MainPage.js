import React, { Component } from "react";
import { get_reduced_urls, delete_reduced_urls } from '../action/actions'
import { connect } from "react-redux";
import Header from "./Header";
import { AiFillDelete } from 'react-icons/ai'
import { GrLink } from 'react-icons/gr'


// NOTES
// Use react icons
// https://react-icons.github.io/react-icons

class MainPage extends Component {


  state = {
    page_num: 1
  }

  componentDidMount = () => {
    this.props.get_reduced_urls(this.state.page_num)
  }

  setPageNum = (value) => {
    if (value === 'increase' )
      this.setState({ page_num: this.state.page_num + 1})
    else if (value === 'decrease' )
      this.setState({ page_num: this.state.page_num - 1 })
  }

  componentDidUpdate = (prevProps, prevState) => {
    if (prevState.page_num !== this.state.page_num){
      this.props.get_reduced_urls(this.state.page_num)
    }
  }

  render() {

    const { page_num } = this.state
    const {
            // VARs
            reduced_urls,

            // FUNC
            delete_reduced_urls} = this.props

    return (
    <React.Fragment>

      <Header location={'mainpage'}/>


      <div className='dp-test-url-container'>

        <span>Reduced URLs</span>
        <br/>
        <span><b>URL {reduced_urls.count}</b></span>

        {reduced_urls && <ul>{ reduced_urls.results.map( e=> {  let url = `http://${e.domain}/${e.url}`;
                                                            return <li key={e.url}>
                                                             <div>
                                                                <div>{e.id}    <a href={url}>{url}</a> <GrLink/> {e.url_destination}
                                                                  <div onClick={() => delete_reduced_urls(e.id)}><AiFillDelete/></div></div>
                                                                
                                                             </div>
                                                          </li>})}
                         </ul>}
        <table>
          <tbody>
          <tr>
            <td onClick={()=> { reduced_urls.previous && this.setPageNum('decrease')}}
              className={reduced_urls.previous ? 'db-test-btn-active' : 'db-test-btn-inactive'}>
              Назад
            </td>

            <td style={{ padding: '10px'}}>
              Страница: {page_num}
            </td>

            <td onClick={()=> { reduced_urls.next && this.setPageNum('increase')} }
              className={ reduced_urls.next ? 'db-test-btn-active' : 'db-test-btn-inactive'}>
              Вперед
            </td>
          </tr>
          </tbody>
        </table>
      </div>

    </React.Fragment>)
  }
}


// connect state
function mapStateToProps(state) {
  return {
    reduced_urls: state.reduced_urls,
  };
}

// dispatch data
function mapDispatchToProps(dispatch) {
  return {
    get_reduced_urls: (page_num) => dispatch(get_reduced_urls(page_num)),
    delete_reduced_urls: (id) => dispatch(delete_reduced_urls(id)),
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(MainPage);
