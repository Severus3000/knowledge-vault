import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { fetchFile } from "../api";
import type { FileContent } from "../types";

interface ArticleViewerProps {
  path: string;
  onNavigate: (path: string) => void;
}

export function ArticleViewer({ path, onNavigate }: ArticleViewerProps) {
  const [file, setFile] = useState<FileContent | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setFile(null);
    setError(null);
    fetchFile(path)
      .then(setFile)
      .catch(() => setError("Failed to load file"));
  }, [path]);

  if (error) return <div style={{ color: "#ef4444" }}>{error}</div>;
  if (!file) return <div style={{ color: "#9ca3af" }}>Loading...</div>;

  const fm = file.frontmatter;

  return (
    <div>
      {fm.title ? <h1 style={{ marginBottom: 8 }}>{String(fm.title)}</h1> : null}
      {fm.tags ? (
        <div style={{ marginBottom: 16, display: "flex", gap: 6, flexWrap: "wrap" }}>
          {(fm.tags as string[]).map((tag) => (
            <span
              key={tag}
              style={{
                background: "#e5e7eb",
                padding: "2px 8px",
                borderRadius: 4,
                fontSize: 12,
              }}
            >
              {tag}
            </span>
          ))}
        </div>
      ) : null}
      {fm.source ? (
        <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 16 }}>
          Source: <a href={String(fm.source)} target="_blank" rel="noreferrer">{String(fm.source)}</a>
        </div>
      ) : null}
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ href, children }) => {
            if (href && !href.startsWith("http")) {
              return (
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    onNavigate(href);
                  }}
                  style={{ color: "#2563eb", textDecoration: "underline", cursor: "pointer" }}
                >
                  {children}
                </a>
              );
            }
            return <a href={href} target="_blank" rel="noreferrer">{children}</a>;
          },
        }}
      >
        {file.body}
      </ReactMarkdown>
    </div>
  );
}
