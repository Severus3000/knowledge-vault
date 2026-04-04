import { useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { ArticleViewer } from "./components/ArticleViewer";
import { ChatPanel } from "./components/ChatPanel";
import { StatusBar } from "./components/StatusBar";
import "./styles/global.css";

export default function App() {
  const [activePath, setActivePath] = useState<string | null>(null);

  return (
    <div className="app-layout">
      <Sidebar activePath={activePath} onSelect={setActivePath} />
      <div className="main-content">
        {activePath ? (
          <ArticleViewer path={activePath} onNavigate={setActivePath} />
        ) : (
          <p style={{ color: "#9ca3af", marginTop: 40, textAlign: "center" }}>
            Select a file from the sidebar to view it
          </p>
        )}
      </div>
      <ChatPanel fileContext={activePath} />
      <StatusBar />
    </div>
  );
}
