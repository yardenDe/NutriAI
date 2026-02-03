import React, { useState, useEffect } from "react";
import axios from "axios";
import ChatBox from "./components/ChatBox";
import Recommendations from "./components/Recommendations";
import SupplementsList from "./components/SupplementsList";
import Auth from "./components/Auth";

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

function App() {
  const [view, setView] = useState("list");
  const [user, setUser] = useState(localStorage.getItem("username"));

  useEffect(() => {
    const savedUser = localStorage.getItem("username");
    if (savedUser && !user) setUser(savedUser);
  }, [user]);

  const handleLogout = () => {
    localStorage.clear();
    setUser(null);
  };

  if (!user) return <Auth setUser={setUser} />;

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-green-600 text-white shadow">
        <div className="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-xl font-bold">NutriAI</h1>
          <div className="flex items-center gap-6">
            <span className="font-medium"> {user}</span>
            <nav className="flex gap-4">
              <button
                className={`hover:underline ${view === "list" ? "font-bold underline" : ""}`}
                onClick={() => setView("list")}
              >
                Supplements
              </button>
              <button
                className={`hover:underline ${view === "recommend" ? "font-bold underline" : ""}`}
                onClick={() => setView("recommend")}
              >
                Recommendations
              </button>
              <button
                className={`hover:underline ${view === "chat" ? "font-bold underline" : ""}`}
                onClick={() => setView("chat")}
              >
                Chat
              </button>
            </nav>
            <button
              onClick={handleLogout}
              className="ml-4 bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto p-6">
        {view === "chat" && <ChatBox />}
        {view === "recommend" && <Recommendations />}
        {view === "list" && <SupplementsList />}
      </main>
    </div>
  );
}

export default App;
