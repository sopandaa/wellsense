import { useEffect, useState } from "react";
import axios from "axios";

function TeamHeatmap() {
  const [data, setData] = useState({});
  const [dates, setDates] = useState([]);
   




  useEffect(() => {
    fetchHeatmap();
  }, []);

  const fetchHeatmap = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/manager/team-heatmap?manager_id=11&days=7"
      );

        console.log("HEATMAP DATA:", JSON.stringify(res.data, null, 2));

      setData(res.data);

      // extract unique dates
      const allDates = new Set();
      Object.values(res.data).forEach(emp => {
        Object.keys(emp).forEach(date => allDates.add(date));
      });

      setDates(Array.from(allDates).sort());

    } catch (err) {
      console.error(err);
    }
  };

   const getColor = (status) => {
  if (status === "HIGH") return "#ff4d4f";
  if (status === "MODERATE") return "#faad14";
  if (status === "LOW") return "#52c41a";
  return "#f0f0f0";
  };
  

  const Legend = ({ color, label }) => (
  <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
    <div style={{
      width: "14px",
      height: "14px",
      backgroundColor: color,
      borderRadius: "3px"
    }} />
    <span style={{ fontSize: "13px", color: "#555" }}>{label}</span>
  </div>
  );



  const headerStyle = {
  fontSize: "13px",
  fontWeight: "500",
  color: "#888",
  padding: "5px"
};

const employeeStyle = {
  fontWeight: "500",
  fontSize: "14px",
  paddingRight: "10px"
};



return (

     





  <div style={{
    background: "#fff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
    marginTop: "20px"
  }}>
    
    <h2 style={{
      fontSize: "20px",
      fontWeight: "600",
      marginBottom: "15px"
    }}>
      Team Health Heatmap
    </h2>

    {/* Legend */}
    <div style={{ marginBottom: "10px", display: "flex", gap: "10px" }}>
      <Legend color="#52c41a" label="Low" />
      <Legend color="#faad14" label="Moderate" />
      <Legend color="#ff4d4f" label="High" />
      <Legend color="#d9d9d9" label="No Data" />
    </div>

    <div style={{ overflowX: "auto" }}>
      <table style={{
        borderCollapse: "separate",
        borderSpacing: "6px"
      }}>
        <thead>
          <tr>
            <th style={headerStyle}>Employee</th>
            {dates.map(date => (
              <th key={date} style={headerStyle}>{date.slice(5)}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {Object.entries(data).map(([empId, records]) => (
            <tr key={empId}>
              <td style={employeeStyle}>
                Emp {empId}
              </td>

              {dates.map(date => (
                <td key={date}>
                  <div
                    style={{
                      width: "28px",
                      height: "28px",
                      borderRadius: "6px",
                      backgroundColor: getColor(records[date]),
                      transition: "0.2s",
                    }}
                    title={`${date} - ${records[date]}`}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);
    
     
}
 

export default TeamHeatmap;