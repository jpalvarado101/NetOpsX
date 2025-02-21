import axios from 'axios';

const API_BASE_URL = "http://localhost:8000";

export const getTransactions = async () => {
  const response = await axios.get(`${API_BASE_URL}/transactions`);
  return response.data;
};

export const manualOverride = async (id: number, new_route: string) => {
  const response = await axios.post(`${API_BASE_URL}/transactions/override`, { id, new_route });
  return response.data;
};
