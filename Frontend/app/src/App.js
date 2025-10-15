import React, { useState } from "react";
import ChatBox from "./components/ChatBox";
import Recommendations from "./components/Recommendations";
import SupplementsList from "./components/SupplementsList";

function App() {
  const [view, setView] = useState("list");

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Title */}
      <header className="bg-green-600 text-white shadow">
        <div className="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-xl font-bold">NutriAI</h1>
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
        </div>
      </header>

      {/* Body */}
      <main className="max-w-5xl mx-auto p-6">
        {view === "chat" && <ChatBox />}
        {view === "recommend" && <Recommendations />}
        {view === "list" && <SupplementsList />}
      </main>
    </div>
  );
}

export default App;
