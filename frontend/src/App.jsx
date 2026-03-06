 
import { useState } from "react";
import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/DashboardPage";
import EmployeeProfile from "./pages/EmployeeProfile";

function App() {

  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogin = () => {
    setToken(localStorage.getItem("token"));
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Routes>

      <Route
        path="/"
        element={<Dashboard onLogout={handleLogout} />}
      />

      <Route
        path="/employee/:id"
        element={<EmployeeProfile onLogout={handleLogout} />}
      />

    </Routes>
  );
}

export default App;