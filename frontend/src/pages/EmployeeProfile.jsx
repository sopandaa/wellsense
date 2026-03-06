import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../api/api";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function EmployeeProfile() {

  const { id } = useParams();
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchTrend();
  }, []);

  const fetchTrend = async () => {
    const res = await API.get(`/wellness/employee-trend/${id}`);
    setData(res.data);
  };

  return (

    <div className="min-h-screen bg-gray-100 p-8">

      <h1 className="text-3xl font-bold mb-8">
        Employee Wellness Trend
      </h1>

      <div className="bg-white p-6 rounded-xl shadow-md">

        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="date" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="sleep"
              stroke="#22c55e"
              name="Sleep Hours"
            />

            <Line
              type="monotone"
              dataKey="work"
              stroke="#3b82f6"
              name="Work Hours"
            />

            <Line
              type="monotone"
              dataKey="fatigue"
              stroke="#ef4444"
              name="Fatigue Score"
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default EmployeeProfile;