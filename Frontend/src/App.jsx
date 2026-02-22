import { useState } from "react";
import jsPDF from "jspdf";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  const API = "http://127.0.0.1:8000";

  // ---------------------------
  // Upload File
  // ---------------------------
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setFileName(file.name);

    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch(`${API}/upload`, {
        method: "POST",
        body: formData,
      });
    } catch (error) {
      console.error("Upload failed:", error);
    }

    setUploading(false);
  };

  // ---------------------------
  // Send Message
  // ---------------------------
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    setLoading(true);
    setInput("");

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();

      const botMsg = { role: "bot", text: data.response };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Chat error:", err);
    }

    setLoading(false);
  };

  // ---------------------------
  // Clear Chat
  // ---------------------------
  const clearChat = () => {
    setMessages([]);
  };

  // ---------------------------
  // Download Chat as PDF
  // ---------------------------
  const downloadChat = () => {
    const doc = new jsPDF();

    let y = 10;

    messages.forEach((msg) => {
      const text = `${msg.role.toUpperCase()}: ${msg.text}`;
      const lines = doc.splitTextToSize(text, 180);
      doc.text(lines, 10, y);
      y += lines.length * 8;
    });

    doc.save("chat-history.pdf");
  };

  return (
    <div className={darkMode ? "app dark" : "app"}>
      <h1>📄 AI Document Assistant</h1>

      {/* Dark Mode Toggle */}
      <button
        className="toggle-btn"
        onClick={() => setDarkMode(!darkMode)}
      >
        {darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
      </button>

      {/* Upload Section */}
      <div className="upload-section">
        <input type="file" onChange={handleFileUpload} />

        {uploading && <p className="status">⏳ Uploading and indexing...</p>}

        {fileName && !uploading && (
          <p className="status">
            📄 Active Document: <b>{fileName}</b>
          </p>
        )}
      </div>

      {/* Chat Window */}
      <div className="chat-container">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.text}
          </div>
        ))}

        {loading && <div className="loader">Thinking...</div>}
      </div>

      {/* Input Section */}
      <div className="input-section">
        <input
          type="text"
          placeholder="Ask something from the document..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />

        <button onClick={sendMessage}>Send</button>
        <button className="clear-btn" onClick={clearChat}>Clear</button>
        <button className="download-btn" onClick={downloadChat}>
          Download PDF
        </button>
      </div>
    </div>
  );
}

export default App;
