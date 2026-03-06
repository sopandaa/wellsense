import { useNavigate } from "react-router-dom";


function EmployeeTable({ employees }) {

  const getRiskColor = (risk) => {
    if (risk === "HIGH") return "text-red-600";
    if (risk === "MODERATE") return "text-yellow-600";
    return "text-green-600";
  };

  const navigate = useNavigate();

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
          {employees.map((emp, index) => (
             <tr
              key={index}
              className="border-t cursor-pointer hover:bg-gray-100"
              onClick={() => navigate(`/employee/${emp.employee_id}`)}
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