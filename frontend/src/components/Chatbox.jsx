import React, { useState, useEffect, useRef } from "react";
import { sendMessage } from "../utils/api";
import Message from "./Message";
import "../styles.css";

const Chatbox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);

    const response = await sendMessage(input);
    setLoading(false);

    const botMessage = response.error
      ? { text: response.error, sender: "bot", error: true }
      : { text: response.response, sender: "bot" };

    setMessages((prevMessages) => [...prevMessages, botMessage]);
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <Message
            key={index}
            text={msg.text}
            sender={msg.sender}
            error={msg.error}
          />
        ))}
        {loading && <Message text="Typing..." sender="bot" />}
        <div ref={chatEndRef} />
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbox;

