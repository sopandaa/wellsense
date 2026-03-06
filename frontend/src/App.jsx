 
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import EmployeeProfile from "./pages/EmployeeProfile";

function App() {

  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogin = () => {
    setToken(localStorage.getItem("token"));
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Dashboard onLogout={logout} />} />

        <Route path="/employee/:id" element={<EmployeeProfile />} />

      </Routes>

    </BrowserRouter>
  );
}

export default App;