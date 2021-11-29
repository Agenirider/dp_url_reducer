import React, { Component } from "react";
import { set_show_notify_modal } from '../action/actions'
import { connect } from "react-redux";


// NOTES
// Use react icons
// https://react-icons.github.io/react-icons

class NotyfyModal extends Component {
  render() {

    const {
        // VARs
        network_message,

        // FUNC
        set_show_notify_modal,
        } = this.props

    const message_decoder = (network_message) => {
        switch (network_message){
            case 'url_created':
                return (<div className='dp-test-modal'
                            style={{ background: 'green'}}>
                            <div>URL успешно создан</div>
                            <div className='db-test-btn-active'
                                 style={{margin: '10px 40px'}}
                                 onClick={() => set_show_notify_modal(false)}>Ок</div>
                            </div>)
            case 'url_already_exists':
                return (<div className='dp-test-modal'
                            style={{ background: 'red'}}>
                            <div>URL уже существует, попробуйте другой вариант</div>
                            <div className='db-test-btn-inactive'
                                style={{margin: '10px 40px'}}
                                onClick={() => set_show_notify_modal(false)}>Ок</div>
                        </div>)
        }
    }

    return (
        <React.Fragment>
            {message_decoder(network_message)}
        </React.Fragment>
    );
    }
}


// connect state
function mapStateToProps(state) {
    return {
        network_message: state.network_message,
    };
}

  // dispatch data
function mapDispatchToProps(dispatch) {
    return {
        set_show_notify_modal: (status) => dispatch(set_show_notify_modal(status))
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(NotyfyModal);
