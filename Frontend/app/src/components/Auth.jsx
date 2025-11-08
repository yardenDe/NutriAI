import React, { useState } from "react";
import axios from "axios";

export default function Auth({ setUser }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    setMessage("");
    if (!username || !password) {
      setMessage("Please fill all fields");
      return;
    }

    const endpoint = isLogin ? "login" : "register";

    try {
      const res = await axios.post(`http://127.0.0.1:8000/${endpoint}`, {
        unique_name: username,
        password: password,
      });

      if (res.data.status === "ok" && res.data.token) {
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("username", username);
        setMessage(isLogin ? "Login successful!" : "Registration successful!");
        setUser(username);
      } else {
        // אם השרת החזיר משהו אחר (למשל {"status": "user exists"})
        setMessage(res.data.status || "Unexpected response");
      }
    } catch (err) {
      console.error("Error:", err);

      // נבדוק אם לשרת הייתה תגובה תקינה עם detail
      if (err.response) {
        const serverMsg =
          err.response.data?.detail || err.response.data?.status;
        setMessage(serverMsg || `Error ${err.response.status}`);
      } else {
        setMessage("Network or server error");
      }
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-xl shadow-lg w-80 space-y-4">
        <h2 className="text-xl font-semibold text-center text-green-600">
          {isLogin ? "Login" : "Register"}
        </h2>

        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          className="w-full border px-3 py-2 rounded-lg"
        />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          type="password"
          className="w-full border px-3 py-2 rounded-lg"
        />

        <button
          onClick={handleSubmit}
          className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition"
        >
          {isLogin ? "Login" : "Register"}
        </button>

        {message && (
          <p
            className={`text-center text-sm ${
              message.toLowerCase().includes("success")
                ? "text-green-600"
                : "text-red-500"
            }`}
          >
            {message}
          </p>
        )}

        <p className="text-sm text-center text-gray-600">
          {isLogin ? "No account?" : "Already registered?"}{" "}
          <button
            onClick={() => {
              setIsLogin(!isLogin);
              setMessage("");
            }}
            className="text-green-600 underline"
          >
            {isLogin ? "Register here" : "Login here"}
          </button>
        </p>
      </div>
    </div>
  );
}
