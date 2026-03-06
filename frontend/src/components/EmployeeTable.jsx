import { useNavigate } from "react-router-dom";

function EmployeeTable({ employees }) {

  const navigate = useNavigate();

  const getRiskColor = (risk) => {
    if (risk === "HIGH") return "text-red-600";
    if (risk === "MODERATE") return "text-yellow-600";
    return "text-green-600";
  };

  if (!employees || employees.length === 0) {
    return <p className="text-gray-500">No employees found.</p>;
  }

  return (
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
          {employees.map((emp) => (
            <tr
              key={emp.employee_id}
              onClick={() => navigate(`/employee/${emp.employee_id}`)}
              className="cursor-pointer hover:bg-gray-50"
            >
              <td className="p-4">{emp.name}</td>
              <td className="p-4">{emp.department}</td>

              <td className="p-4 font-bold">
                {emp.burnout_score}
              </td>

              <td className={`p-4 font-bold ${getRiskColor(emp.risk_level)}`}>
                {emp.risk_level}
              </td>
            </tr>
          ))}
        </tbody>

      </table>
    </div>
  );
}

export default EmployeeTable;