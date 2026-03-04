import { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  PieChart,
  Pie,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Dashboard({ token, onLogout }) {
  const [departments, setDepartments] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [trendData, setTrendData] = useState([]);
  const [riskData, setRiskData] = useState([]);

  useEffect(() => {
    fetchDepartmentRisk();
    fetchEmployeeRisk();
    fetchTrend();
    fetchRiskDistribution();
  }, []);

  const authHeader = {
    headers: { Authorization: `Bearer ${token}` },
  };

  const fetchDepartmentRisk = async () => {
    const res = await axios.get(
      "http://127.0.0.1:8000/wellness/department-risk",
      authHeader
    );
    setDepartments(res.data);
  };

  const fetchEmployeeRisk = async () => {
    const res = await axios.get(
      "http://127.0.0.1:8000/wellness/employee-risk",
      authHeader
    );
    const sorted = res.data.sort(
      (a, b) => b.burnout_score - a.burnout_score
    );
    setEmployees(sorted.slice(0, 5));
  };

  const fetchTrend = async () => {
    const res = await axios.get(
      "http://127.0.0.1:8000/wellness/company-trend",
      authHeader
    );
    setTrendData(res.data);
  };

  const fetchRiskDistribution = async () => {
    const res = await axios.get(
      "http://127.0.0.1:8000/wellness/risk-distribution",
      authHeader
    );

    setRiskData([
      { name: "LOW", value: res.data.LOW, fill: "#22c55e" },
      { name: "MODERATE", value: res.data.MODERATE, fill: "#eab308" },
      { name: "HIGH", value: res.data.HIGH, fill: "#ef4444" },
    ]);
  };

  const getRiskColor = (risk) => {
    if (risk === "HIGH") return "text-red-600";
    if (risk === "MODERATE") return "text-yellow-600";
    return "text-green-600";
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <Navbar onLogout={onLogout} />

      {/* Trend Chart */}
      <h2 className="text-2xl font-bold mb-6">
        Company Burnout Trend (14 Days)
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

      {/* Risk Pie */}
      <h2 className="text-2xl font-bold mb-6">
        Company Risk Distribution
      </h2>

      <div className="bg-white p-6 rounded-xl shadow-md mb-10">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={riskData}
              dataKey="value"
              nameKey="name"
              outerRadius={100}
            />
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Department Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {departments.map((dept, i) => (
          <div key={i} className="bg-white shadow-md rounded-xl p-6">
            <h2 className="text-xl font-semibold">
              {dept.department}
            </h2>
            <p>Avg Burnout: {dept.avg_burnout_score}</p>
            <p className={getRiskColor(dept.risk_level)}>
              {dept.risk_level}
            </p>
          </div>
        ))}
      </div>

      {/* Top 5 Employees */}
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
            {employees.map((emp, i) => (
              <tr key={i} className="border-t">
                <td className="p-4">{emp.name}</td>
                <td className="p-4">{emp.department}</td>
                <td className="p-4 font-bold">
                  {emp.burnout_score}
                </td>
                <td className={`p-4 ${getRiskColor(emp.risk_level)}`}>
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

export default Dashboard;