import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    const response = await axios.get(
      "http://127.0.0.1:5000/history"
    );

    setHistory(response.data);
  };

  const totalScans = history.length;

  const safeCount = history.filter(
    item => item.result === "Safe"
  ).length;

  const suspiciousCount = history.filter(
    item => item.result === "Suspicious"
  ).length;

  return (
    <div className="container mt-5">

      <h2>CyberShield Dashboard</h2>

      <div className="row mt-4">

        <div className="col-md-4">
          <div className="card p-3 shadow">
            <h5>Total Scans</h5>
            <h2>{totalScans}</h2>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card p-3 shadow">
            <h5>Safe URLs</h5>
            <h2>{safeCount}</h2>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card p-3 shadow">
            <h5>Threat URLs</h5>
            <h2>{suspiciousCount}</h2>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;