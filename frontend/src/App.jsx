 
import { useEffect, useState } from "react";
import axios from "axios";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";


function App() {
  const [departments, setDepartments] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  const [trendData, setTrendData] = useState([]);


  useEffect(() => {
    if (token) {
      fetchDepartmentRisk();
      fetchEmployeeRisk();

      fetchTrend();

    }
  }, [token]);

  const login = async () => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/login?email=${email}&password=${password}`
    );

    localStorage.setItem("token", response.data.access_token);
    setToken(response.data.access_token);
  } catch (error) {
    alert("Invalid email or password");
  }
};

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  const fetchDepartmentRisk = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/wellness/department-risk",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setDepartments(response.data);
    } catch (error) {
      alert("Token expired. Please login again.");
      logout();
    }
  };

  const fetchEmployeeRisk = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/wellness/employee-risk",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const sorted = response.data.sort(
        (a, b) => b.burnout_score - a.burnout_score
      );

      setEmployees(sorted.slice(0, 5));
    } catch (error) {
      logout();
    }
  };

  const getRiskColor = (risk) => {
    if (risk === "HIGH") return "text-red-600";
    if (risk === "MODERATE") return "text-yellow-600";
    return "text-green-600";
  };



const fetchTrend = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/wellness/company-trend",
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    setTrendData(response.data);
  } catch (error) {
    console.error("Error fetching trend:", error);
  }
};





  // ================= LOGIN SCREEN =================
  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-xl shadow-md w-96">
          <h2 className="text-2xl font-bold mb-6 text-center">
            HR Login
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
            onClick={login}
            className="w-full bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
          >
            Login
          </button>
        </div>
      </div>
    );
  }

  // ================= DASHBOARD =================
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          HR Wellness Dashboard
        </h1>

        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>




  <h2 className="text-2xl font-bold mb-6 text-gray-800">
  Company Burnout Trend (Last 14 Days)
  </h2>

  <div className="bg-white p-6 rounded-xl shadow-md mb-10">
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={trendData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line 
        type="monotone" 
        dataKey="avg_burnout" 
        stroke="#ef4444" 
        strokeWidth={3} 
      />
    </LineChart>
  </ResponsiveContainer>
  </div>




      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {departments.map((dept, index) => (
          <div
            key={index}
            className="bg-white shadow-md rounded-xl p-6"
          >
            <h2 className="text-xl font-semibold">
              {dept.department}
            </h2>

            <p className="mt-2">
              Avg Burnout: {dept.avg_burnout_score}
            </p>

            <p className={`mt-2 font-bold ${getRiskColor(dept.risk_level)}`}>
              {dept.risk_level}
            </p>

            <p className="mt-2">
              Employees: {dept.employee_count}
            </p>
          </div>
        ))}
      </div>

      <h2 className="text-2xl font-bold mt-12 mb-6">
        Top 5 High-Risk Employees
      </h2>

      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-4">Employee</th>
              <th className="p-4">Department</th>
              <th className="p-4">Burnout</th>
              <th className="p-4">Risk</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((emp, index) => (
              <tr key={index} className="border-t">
                <td className="p-4">{emp.name}</td>
                <td className="p-4">{emp.department}</td>
                <td className="p-4 font-bold">
                  {emp.burnout_score}
                </td>
                <td
                  className={`p-4 font-bold ${getRiskColor(
                    emp.risk_level
                  )}`}
                >
                  {emp.risk_level}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;