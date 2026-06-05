import { useState } from "react";

function URLChecker() {
  const [url, setUrl] = useState("");

  const handleAnalyze = () => {
    alert(`Analyzing: ${url}`);
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
      </div>
    </div>
  );
}

export default URLChecker;