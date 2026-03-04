import { useState } from "react";
import axios from "axios";

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");



  const handleLogin = async () => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/login",
      null,
      {
        params: {
          email: email,
          password: password,
        },
      }
    );

    const token = response.data.access_token;

    localStorage.setItem("token", token);
    onLogin(token);

  } catch (err) {
    console.log(err.response?.data);
    setError("Invalid credentials");
  }
};



  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Login to WellSense AI
        </h2>

        <input
          type="text"
          placeholder="Email"
          className="w-full p-3 mb-4 border rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 mb-4 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
        >
          Login
        </button>

        {error && (
          <p className="text-red-500 mt-4 text-center">
            {error}
          </p>
        )}
      </div>
    </div>
  );
}

export default Login; 