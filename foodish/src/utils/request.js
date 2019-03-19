import axios from "axios";
const requst = axios.create({});
requst.interceptors.request.use(async config => {
  config.headers = config.headers || {}
  let token = ''
  try {
    token = JSON.parse(window.localStorage.getItem('users')) || {}
    token = token.token
  } catch (error) {

  }
  config.headers['Authorization'] = `Token ${token}`
  return config
})

requst.interceptors.response.use(response => {
  return response;
}, error => {
  try {
    if (error.response.data.detail === 'Signature has expired.') {
      window.localStorage.setItem('users', "");
      window.location.href = '/'
    }
  } catch (error) {

  }
  return response;
})
export default requst;
