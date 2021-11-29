import {
  GET_REDUCED_URLS,
  SET_NETWORK_MESSAGE,
  SET_ONLOADING,
  SET_SHOW_NOTIFY_MODAL,

  } from './action/actionTypes'

  const initialState = {
    reduced_urls: false,
    network_message: false,
    onLoading: false,
    show_notify_modal: false

  }

  export default (state = initialState, action) => {
    switch (action.type) {

      case GET_REDUCED_URLS:
        return {
          ...state,
          reduced_urls: action.payload,
        };

      case SET_NETWORK_MESSAGE:
        return {
          ...state,
          network_message: action.payload.res,
          show_notify_modal: true
        };

      case SET_ONLOADING:
        return {
          ...state,
          onLoading: action.payload,
        };

      case SET_SHOW_NOTIFY_MODAL:
        return {
          ...state,
          show_notify_modal: action.payload
        };

      default:
        return state
    }
  }