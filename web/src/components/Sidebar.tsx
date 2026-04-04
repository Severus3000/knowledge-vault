import { useEffect, useState } from "react";
import { fetchTree } from "../api";
import type { VaultTree } from "../types";
import { GraphView } from "./GraphView";

interface SidebarProps {
  activePath: string | null;
  onSelect: (path: string) => void;
}

export function Sidebar({ activePath, onSelect }: SidebarProps) {
  const [tree, setTree] = useState<VaultTree | null>(null);
  const [showGraph, setShowGraph] = useState(false);

  useEffect(() => {
    fetchTree().then(setTree).catch(console.error);
  }, []);

  if (!tree) return <div className="sidebar">Loading...</div>;

  const renderSection = (label: string, files: VaultTree[keyof VaultTree]) => (
    <div className="file-tree-section">
      <h3>{label} ({files.length})</h3>
      {files.map((f) => (
        <div
          key={f.path}
          className={`file-tree-item ${activePath === f.path ? "active" : ""}`}
          onClick={() => onSelect(f.path)}
          title={f.path}
        >
          {f.dir ? `${f.dir}/` : ""}{f.name}
        </div>
      ))}
    </div>
  );

  return (
    <div className="sidebar">
      <div style={{ marginBottom: 12, display: "flex", gap: 8 }}>
        <button
          onClick={() => setShowGraph(false)}
          style={{
            flex: 1, padding: "4px 8px", fontSize: 12, cursor: "pointer",
            background: showGraph ? "transparent" : "#e5e7eb", border: "1px solid #d1d5db", borderRadius: 4,
          }}
        >
          Files
        </button>
        <button
          onClick={() => setShowGraph(true)}
          style={{
            flex: 1, padding: "4px 8px", fontSize: 12, cursor: "pointer",
            background: showGraph ? "#e5e7eb" : "transparent", border: "1px solid #d1d5db", borderRadius: 4,
          }}
        >
          Graph
        </button>
      </div>
      {showGraph ? (
        <GraphView onNodeClick={onSelect} />
      ) : (
        <>
          {renderSection("Wiki", tree.wiki)}
          {renderSection("Raw", tree.raw)}
          {renderSection("Outputs", tree.outputs || [])}
        </>
      )}
    </div>
  );
}
