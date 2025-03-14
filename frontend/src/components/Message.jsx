import React from "react";

const Message = ({ text, sender, error }) => {
  return (
    <div className={`message ${sender} ${error ? "error" : ""}`}>{text}</div>
  );
};

export default Message;
