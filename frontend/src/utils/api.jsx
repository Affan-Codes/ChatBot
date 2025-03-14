import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000/api";

export const sendMessage = async (message) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, { message });
    return response.data;
  } catch (error) {
    console.error(
      "API Error:",
      error.response ? error.response.data : error.message
    );
    return { error: "Failed to get response from server" };
  }
};
