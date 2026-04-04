import { useState, useRef, useEffect, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { createChatSocket } from "../api";
import type { ChatMessage } from "../types";

interface ChatPanelProps {
  fileContext: string | null;
}

export function ChatPanel({ fileContext }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const connectWs = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;
    const ws = createChatSocket();

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "done") {
        setIsStreaming(false);
        return;
      }
      if (data.type === "text" || data.type === "result") {
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last && last.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { ...last, content: last.content + (data.content || "") },
            ];
          }
          return [...prev, { role: "assistant", content: data.content || "", timestamp: Date.now() }];
        });
      }
    };

    ws.onclose = () => {
      wsRef.current = null;
    };

    wsRef.current = ws;
  }, []);

  const sendMessage = () => {
    if (!input.trim() || isStreaming) return;
    connectWs();

    const userMsg: ChatMessage = { role: "user", content: input, timestamp: Date.now() };
    setMessages((prev) => [...prev, userMsg]);
    setIsStreaming(true);

    const send = () => {
      wsRef.current?.send(
        JSON.stringify({ message: input, file_context: fileContext })
      );
    };

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      send();
    } else {
      wsRef.current!.onopen = send;
    }

    setInput("");
  };

  return (
    <div className="chat-panel">
      <div style={{ padding: "12px 16px", borderBottom: "1px solid #e5e7eb", fontWeight: 600, fontSize: 13 }}>
        Chat
      </div>
      <div style={{ flex: 1, overflowY: "auto", padding: 16 }}>
        {messages.length === 0 && (
          <p style={{ color: "#9ca3af", fontSize: 13 }}>
            Ask a question about your knowledge vault, paste a URL to ingest, or type "compile" to run the compiler.
          </p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              marginBottom: 16,
              padding: "8px 12px",
              borderRadius: 8,
              background: msg.role === "user" ? "#dbeafe" : "#f3f4f6",
              maxWidth: "95%",
              marginLeft: msg.role === "user" ? "auto" : 0,
            }}
          >
            {msg.role === "assistant" ? (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
            ) : (
              <p style={{ margin: 0 }}>{msg.content}</p>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div style={{ padding: 12, borderTop: "1px solid #e5e7eb", display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
          placeholder="Ask a question or paste a URL..."
          disabled={isStreaming}
          style={{
            flex: 1,
            padding: "8px 12px",
            border: "1px solid #d1d5db",
            borderRadius: 6,
            fontSize: 13,
            outline: "none",
          }}
        />
        <button
          onClick={sendMessage}
          disabled={isStreaming || !input.trim()}
          style={{
            padding: "8px 16px",
            background: isStreaming ? "#9ca3af" : "#2563eb",
            color: "#fff",
            border: "none",
            borderRadius: 6,
            cursor: isStreaming ? "default" : "pointer",
            fontSize: 13,
          }}
        >
          {isStreaming ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
