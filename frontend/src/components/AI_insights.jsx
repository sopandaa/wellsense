import { useEffect, useState } from "react";
import API from "../api/api";

function AIInsights() {

  const [insights, setInsights] = useState([]);

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    const res = await API.get("/wellness/ai-insights");
    setInsights(res.data.insights);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md mb-10">

      <h2 className="text-xl font-bold mb-4">
        AI Burnout Insights
      </h2>

      {insights.length === 0 ? (
        <p className="text-gray-500">
          No risk signals detected.
        </p>
      ) : (
        <ul className="space-y-2">
          {insights.map((item, index) => (
            <li
              key={index}
              className="text-red-600 font-medium"
            >
              ⚠ {item}
            </li>
          ))}
        </ul>
      )}

    </div>
  );
}

export default AIInsights;