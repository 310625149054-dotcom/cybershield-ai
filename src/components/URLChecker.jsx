import { useState } from "react";
import axios from "axios";

function URLChecker() {
  const API_URL =
    import.meta.env.VITE_API_URL ||
    "https://cybershield-ai-g1m4.onrender.com";

  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);

  const analyzeURL = async () => {
    try {
      const response = await axios.post(
        `${API_URL}/analyze`,
        {
          url: url,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Backend connection failed");
    }
  };

  return (
    <div className="container mt-5">
      <h1>Phishing URL Checker</h1>

      <input
        className="form-control mt-3"
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button
        className="btn btn-danger mt-3"
        onClick={analyzeURL}
      >
        Analyze URL
      </button>

      {result && (
        <div className="mt-4">
          <h4>Result</h4>
          <p><b>URL:</b> {result.url}</p>
          <p><b>Risk:</b> {result.risk}</p>
          <p><b>Status:</b> {result.result}</p>
          <p><b>Explanation:</b> {result.explanation}</p>
        </div>
      )}
    </div>
  );
}

export default URLChecker;