import Axios from "axios";

import {
    GET_REDUCED_URLS,
    SET_NETWORK_MESSAGE,
    SET_ONLOADING,
    SET_SHOW_NOTIFY_MODAL
} from "./actionTypes";


import BASE_URL from "../../config/config";
const API_client = Axios.create()
API_client.defaults.withCredentials = true;


const api_interactions_interceptor = (dispatch) => {

    API_client.interceptors.request.use(
      (request) => {
        dispatch({ type: SET_ONLOADING, payload: true });
        return Promise.resolve(request);
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    API_client.interceptors.response.use(
      (response) => {
        dispatch({ type: SET_ONLOADING, payload: false })
        return Promise.resolve(response)
      },
      (error) => {
        let status_code;
        try {
          status_code = error.response.status;
        } catch {
          status_code = error.message;
        }
        dispatch({ type: SET_NETWORK_MESSAGE, payload: error.response.data });
        dispatch({ type: SET_ONLOADING, payload: false })

        return Promise.reject(error);
      }
    );
};

export const get_reduced_urls = (page_num) => dispatch => {
    api_interactions_interceptor(dispatch)
    API_client.get(`http://${BASE_URL}/url_reducer/get_url/page=${page_num}`)
      .then((response) => {
          dispatch({ type: GET_REDUCED_URLS, payload: response.data });
      }
    );
}

export const delete_reduced_urls = (url_id) => dispatch => {
  api_interactions_interceptor(dispatch)
  API_client.delete(`http://${BASE_URL}/url_reducer/delete_url/${url_id}`)
    .then(() => {
        dispatch(get_reduced_urls(0));
    }
  );
}

export const set_reduced_urls = (domain_id, url_custom, url_destination) => dispatch => {
  api_interactions_interceptor(dispatch)
  API_client.post(`http://${BASE_URL}/url_reducer/set_url`,
       { url_destination : url_destination,
         domain: domain_id,
         url: url_custom })
    .then((response) => {
        let response_status = response.data;
        dispatch({ type: SET_NETWORK_MESSAGE, payload: response_status });
        dispatch(get_reduced_urls(0));
    }
  );
}

export const set_show_notify_modal = (status) => dispatch => {
  dispatch({ type: SET_SHOW_NOTIFY_MODAL, payload: status })
}