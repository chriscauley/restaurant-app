import axios from "axios";

function handleError(error) {
  throw error;
}

const api = axios.create({ baseURL: "/api" });
api.interceptors.response.use(r => r.data, handleError);

export default api;
