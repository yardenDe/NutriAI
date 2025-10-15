import React, { useEffect, useState } from "react";
import axios from "axios";

export default function SupplementsList() {
  const [supps, setSupps] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/supplements")
      .then((res) => setSupps(res.data))
      .catch((err) => console.error("Error fetching supplements:", err));
  }, []);

  return (
    <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {supps.map((s, i) => (
        <div key={i} className="bg-white p-4 shadow rounded-lg hover:shadow-md transition">
          <h4 className="font-bold text-green-600">{s.name}</h4>
          <p className="text-sm text-gray-700">{s.description}</p>
        </div>
      ))}
    </div>
  );
}
