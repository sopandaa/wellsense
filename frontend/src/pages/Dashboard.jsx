import { useEffect, useState } from "react";
import API from "../api/api";
import Navbar from "../components/Navbar";

import AIInsights from "../components/AI_insights";

import BurnoutTrendChart from "../components/charts/BurnoutTrendChart";
import RiskPieChart from "../components/charts/RiskPieChart";
import DepartmentCard from "../components/DepartmentCard";
import EmployeeTable from "../components/EmployeeTable";

 function Dashboard({ onLogout }) {

  const [departments, setDepartments] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [trendData, setTrendData] = useState([]);
  const [riskData, setRiskData] = useState([]);

  useEffect(() => {
    fetchDepartments();
    fetchEmployees();
    fetchTrend();
    fetchRiskDistribution();
  }, []);

  const fetchDepartments = async () => {
    const res = await API.get("/wellness/department-risk");
    setDepartments(res.data);
  };

  const fetchEmployees = async () => {
    const res = await API.get("/wellness/employee-risk");

    const sorted = res.data.sort(
      (a, b) => b.burnout_score - a.burnout_score
    );

    setEmployees(sorted.slice(0, 5));
  };

  const fetchTrend = async () => {
    const res = await API.get("/wellness/company-trend");
    setTrendData(res.data);
  };

  const fetchRiskDistribution = async () => {
    const res = await API.get("/wellness/risk-distribution");

    const formatted = [
      { name: "LOW", value: res.data.LOW, fill: "#22c55e" },
      { name: "MODERATE", value: res.data.MODERATE, fill: "#eab308" },
      { name: "HIGH", value: res.data.HIGH, fill: "#ef4444" },
    ];

    setRiskData(formatted);
  };

   

  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <Navbar onLogout={onLogout} />


      <AIInsights />


      <h2 className="text-xl font-bold mb-4">
        Burnout Trend
      </h2>

      <BurnoutTrendChart data={trendData} />

      <h2 className="text-xl font-bold mb-4">
        Risk Distribution
      </h2>

      <RiskPieChart data={riskData} />

      <h2 className="text-xl font-bold mb-4">
        Department Risk
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        {departments.map((dept, index) => (
          <DepartmentCard key={index} dept={dept} />
        ))}
      </div>

      <h2 className="text-xl font-bold mb-4">
        Top High Risk Employees
      </h2>

      <EmployeeTable employees={employees} />

    </div>
  );
}

export default Dashboard;