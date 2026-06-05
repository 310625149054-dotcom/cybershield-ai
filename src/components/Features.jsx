function Features() {
  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">
        Features
      </h2>

      <div className="row">

        <div className="col-md-4">
          <div className="card p-3 shadow">
            <h4>URL Analysis</h4>
            <p>Detect suspicious phishing links.</p>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card p-3 shadow">
            <h4>AI Risk Score</h4>
            <p>Generate a threat score for URLs.</p>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card p-3 shadow">
            <h4>Cyber Awareness</h4>
            <p>Educate users about cyber threats.</p>
          </div>
        </div>

      </div>
    </div>
  );
}

export default Features;