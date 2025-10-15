import React, { useState } from "react";
import axios from "axios";
import qs from "qs"; // npm install qs

export default function Recommendations() {
  const [symptomText, setSymptomText] = useState("");
  const [recs, setRecs] = useState([]);
  const [error, setError] = useState(null);

  const fetchRecs = async () => {
    if (!symptomText.trim()) {
      setError("Please enter at least one symptom");
      return;
    }

    const symptomsArray = symptomText.split(",").map((s) => s.trim());

    try {
      const res = await axios.get("http://127.0.0.1:8000/recommendations", {
        params: { symptoms: symptomsArray },
        paramsSerializer: (params) => qs.stringify(params, { arrayFormat: "repeat" }),
      });

      if (res.data.error) {
        setError(res.data.error);
        setRecs([]);
      } else {
        setError(null);
        setRecs(res.data.recommendations || []);
      }
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setError("Request failed");
      setRecs([]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white shadow-lg rounded-xl p-6 space-y-4">
      <div className="flex gap-2">
        <input
          value={symptomText}
          onChange={(e) => setSymptomText(e.target.value)}
          placeholder="Enter symptoms (comma separated)"
          className="flex-1 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-400"
        />
        <button
          onClick={fetchRecs}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg"
        >
          Get
        </button>
      </div>

      {error && <p className="text-red-500">{error}</p>}

      <ul className="space-y-3">
        {recs.map((r, i) => (
          <li key={i} className="p-3 bg-gray-100 rounded-lg shadow">
            <b>{r[1]}</b>: {r[2]}
            <br />
            <small className="text-gray-500">similarity: {r[3]?.toFixed(2)}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
