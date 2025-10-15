import React, { useState } from "react";
import axios from "axios";

export default function ChatBox() {
  const [sessionId] = useState("demo-session");
  const [text, setText] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!text.trim()) return;
    const newMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, newMessage]);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        session_id: sessionId,
        text: text,
      });
      const reply = { role: "assistant", content: res.data.answer };
      setMessages((prev) => [...prev, reply]);
    } catch (err) {
      console.error("Error:", err);
      const reply = { role: "assistant", content: " Server error" };
      setMessages((prev) => [...prev, reply]);
    }

    setText("");
  };

  return (
    <div className="flex flex-col h-[70vh] max-w-2xl mx-auto bg-white shadow-xl rounded-xl">
      <div className="flex-1 p-4 overflow-y-auto space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`px-4 py-2 rounded-2xl max-w-[70%] ${
                m.role === "user" ? "bg-green-200 text-right" : "bg-gray-200 text-left"
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
      </div>
      <div className="p-4 border-t flex gap-2">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
          className="flex-1 border rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-400"
        />
        <button
          onClick={sendMessage}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}
