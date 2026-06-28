import { useState, useEffect } from "react";
import axios from "axios";

function URLChecker() {
  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const loadHistory = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/history`
      );

      setHistory(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleAnalyze = async () => {
    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        url
      });

      setResult(response.data);
      loadHistory();
    } catch (error) {
      console.error(error);
      alert("Backend connection failed");
    }
  };

  return (
    <div className="container mt-5">

      <div className="card shadow p-4">

        <h3>Phishing URL Checker</h3>

        <input
          type="text"
          className="form-control mt-3"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button
          className="btn btn-danger mt-3"
          onClick={handleAnalyze}
        >
          Analyze URL
        </button>

        {result && (
          <div className="mt-4">
            <h5>Risk Score: {result.risk}%</h5>
            <h5>Result: {result.result}</h5>
            <p className="mt-2"><strong>Explanation:</strong> {result.explanation}</p>
          </div>
        )}

        <hr />

        <h4>Scan History</h4>

        <table className="table table-bordered">

          <thead>
            <tr>
              <th>URL</th>
              <th>Risk</th>
              <th>Result</th>
            </tr>
          </thead>

          <tbody>

            {history.map((item, index) => (
              <tr key={index}>
                <td>{item.url}</td>
                <td>{item.risk}</td>
                <td>{item.result}</td>
              </tr>
            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default URLChecker;