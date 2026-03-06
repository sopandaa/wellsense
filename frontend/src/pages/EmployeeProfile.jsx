import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../api/api";
import Navbar from "../components/Navbar";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function EmployeeProfile({ onLogout }) {

  const { id } = useParams();

  const [trend, setTrend] = useState([]);
  const [burnout, setBurnout] = useState(null);

  useEffect(() => {
    fetchTrend();
    fetchRisk();
  }, []);

  const fetchTrend = async () => {
    const res = await API.get(`/wellness/employee-trend/${id}`);
    setTrend(res.data);
  };

  const fetchRisk = async () => {
    const res = await API.get(`/wellness/employee-risk/${id}`);
    setBurnout(res.data);
  };

  if (!burnout) {
    return <div className="p-10">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <Navbar onLogout={onLogout} />

      <h1 className="text-3xl font-bold mb-6">
        Employee ID: {burnout.employee_id}
      </h1>

      <p className="mb-2">
        Risk Level: {burnout.risk_level}
      </p>

      <p className="mb-8">
        Current Burnout Score: {burnout.burnout_score}
      </p>

      <h2 className="text-xl font-bold mb-4">
        Burnout Trend
      </h2>

      <div className="bg-white p-6 rounded-xl shadow-md">

        <ResponsiveContainer width="100%" height={300}>

          <LineChart data={trend}>

            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />

            <Line
              type="monotone"
              dataKey="burnout"
              stroke="#ef4444"
              strokeWidth={3}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default EmployeeProfile;