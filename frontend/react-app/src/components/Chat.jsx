import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./chat.css";
import ChatbotIco from "@/assets/images/Chatbot2.png";
import CustomerIco from "@/assets/images/Customer3.png"; 

// 백엔드에서 보내는 텍스트 내의 "+++" 패턴을 찾아 a 태그로 대체하는 함수
function parseLinkText(text) {
  const regex = /\+\+\+([^+]+)\+\+\+/g;
  return text.replace(regex, (match, p1) => {
    const cleanUrl = p1.trim();
    return `<a href="${cleanUrl}" target="_blank" rel="noopener noreferrer">(링크)</a>`;
  });
}

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!userMessage.trim()) return;

    // 사용자 메시지 추가
    const userMsgObj = { text: userMessage, isUser: true };
    setMessages((prevMessages) => [...prevMessages, userMsgObj]);

    // AI 응답 메시지 초기 상태 (로딩 표시)
    const aiMessageObj = {
      text: "타이핑 중...",
      isUser: false,
      id: Date.now(),
      links: null
    };
    setMessages((prevMessages) => [...prevMessages, aiMessageObj]);

    // 입력창 초기화
    setUserMessage("");

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/chat", {
        user_message: userMessage
      });
      const reply = response.data.reply;
      const links = response.data.links;
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === aiMessageObj.id
            ? { ...msg, text: reply, links: links }
            : msg
        )
      );
    } catch (error) {
      console.error("에러", error);
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === aiMessageObj.id
            ? { ...msg, text: "Error occurred" }
            : msg
        )
      );
    }
    setLoading(false);
  };

  return (
    <div className="app" style={{ justifySelf: "center" }}>
      <div className="chat-box">
        <h1 style={{ fontSize: "1.9rem" }}>무엇을 도와드릴까요?</h1>
        <MessageList messages={messages} />
        <MessageForm
          userMessage={userMessage}
          setUserMessage={setUserMessage}
          handleSendMessage={handleSendMessage}
          loading={loading}
        />
      </div>
    </div>
  );
};

const MessageList = ({ messages }) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="messages-list">
      {messages.map((message, index) => (
        <Message key={index} {...message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

const Message = ({ text, isUser, links }) => {
  // AI 메시지의 경우, parseLinkText로 후처리
  const formattedText = !isUser ? parseLinkText(text) : text;

  // 링크 딕셔너리가 있을 경우 첫 번째 링크만 추출
  let singleLink = null;
  if (!isUser && links) {
    const entries = Object.entries(links);
    if (entries.length > 0) {
      const [key, url] = entries[0];
      // 앞뒤 "+++" 제거
      const cleanUrl = url.replace(/^\+\+\+|\+\+\+$/g, "").trim();
      singleLink = (
        <a
          href={cleanUrl}
          target="_blank"
          rel="noopener noreferrer"
          style={{ marginRight: "0.5rem" }}
        >
         
        </a>
      );
    }
  }

  return (
    <div className={isUser ? "user-message" : "ai-message"}>
      <p style={{ display: "flex", alignItems: "center" }}>
        {isUser ? (
          <img src={CustomerIco} className="chat-ico" alt="고객 아이콘" />
        ) : (
          <img src={ChatbotIco} className="chat-ico" alt="챗봇 아이콘" />
        )}
        :{" "}
        <span dangerouslySetInnerHTML={{ __html: formattedText }} />
      </p>
      {/* 단일 링크 렌더링 */}
      {!isUser && singleLink && <div className="links">{singleLink}</div>}
    </div>
  );
};

const MessageForm = ({ userMessage, setUserMessage, handleSendMessage, loading }) => {
  return (
    <form onSubmit={handleSendMessage} className="message-form">
      <input
        type="text"
        value={userMessage}
        onChange={(e) => setUserMessage(e.target.value)}
        className="message-input"
        placeholder="메시지를 입력하세요"
      />
      <button type="submit" className="send-button" disabled={loading}>
        {loading ? "Loading..." : "전송"}
      </button>
    </form>
  );
};

export default Chat;
