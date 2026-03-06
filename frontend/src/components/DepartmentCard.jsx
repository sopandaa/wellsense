function DepartmentCard({ dept }) {

  const getRiskColor = (risk) => {
    if (risk === "HIGH") return "text-red-600";
    if (risk === "MODERATE") return "text-yellow-600";
    return "text-green-600";
  };

  return (
    <div className="bg-white shadow-md rounded-xl p-6">
      <h2 className="text-xl font-semibold">
        {dept.department}
      </h2>

      <p className="mt-2">
        Avg Burnout: {dept.avg_burnout}
      </p>

      <p className={`mt-2 font-bold ${getRiskColor(dept.risk_level)}`}>
        {dept.risk_level}
      </p>

      <p className="mt-2">
        Employees: {dept.employee_count}
      </p>
    </div>
  );
}

export default DepartmentCard;