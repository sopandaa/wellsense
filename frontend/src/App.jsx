 
 import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    fetchDepartmentRisk();
  }, []);

  const fetchDepartmentRisk = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/wellness/department-risk",
        {
          headers: {
            Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYW1AZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjo5LCJyb2xlIjoiSFIiLCJjb21wYW55X2lkIjoyLCJleHAiOjE3NzI1MzIxNDR9.imZ0_dZpyS4caNa6a4eoIiAKu93QYdtux6vcfc81RCo",
          },
        }
      );

      setDepartments(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const getRiskColor = (risk) => {
    if (risk === "HIGH") return "text-red-600";
    if (risk === "MODERATE") return "text-yellow-600";
    return "text-green-600";
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">
        HR Wellness Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {departments.map((dept, index) => (
          <div
            key={index}
            className="bg-white shadow-md rounded-xl p-6 hover:shadow-lg transition"
          >
            <h2 className="text-xl font-semibold text-gray-700">
              {dept.department}
            </h2>

            <p className="mt-3 text-gray-600">
              Avg Burnout Score:
              <span className="ml-2 font-bold">
                {dept.avg_burnout_score}
              </span>
            </p>

            <p className="mt-2 text-gray-600">
              Risk Level:
              <span
                className={`ml-2 font-bold ${getRiskColor(
                  dept.risk_level
                )}`}
              >
                {dept.risk_level}
              </span>
            </p>

            <p className="mt-2 text-gray-600">
              Employees: {dept.employee_count}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;