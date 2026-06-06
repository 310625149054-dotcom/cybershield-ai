import { useState } from "react";
import axios from "axios";

function URLChecker() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/analyze",
        { url }
      );

      setResult(response.data);
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
          </div>
        )}

      </div>
    </div>
  );
}

export default URLChecker;