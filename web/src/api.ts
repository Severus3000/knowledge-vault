import type { VaultTree, FileContent, SearchResult, VaultStats, GraphData } from "./types";

const BASE = "";

export async function fetchTree(): Promise<VaultTree> {
  const res = await fetch(`${BASE}/api/vault/tree`);
  return res.json();
}

export async function fetchFile(path: string): Promise<FileContent> {
  const res = await fetch(`${BASE}/api/vault/read?path=${encodeURIComponent(path)}`);
  if (!res.ok) throw new Error("File not found");
  return res.json();
}

export async function searchVault(query: string): Promise<SearchResult[]> {
  const res = await fetch(`${BASE}/api/vault/search?q=${encodeURIComponent(query)}`);
  const data = await res.json();
  return data.results;
}

export async function fetchStats(): Promise<VaultStats> {
  const res = await fetch(`${BASE}/api/vault/stats`);
  return res.json();
}

export async function fetchGraph(): Promise<GraphData> {
  const res = await fetch(`${BASE}/api/vault/graph`);
  return res.json();
}

export async function ingestContent(body: {
  title: string;
  source: string;
  platform?: string;
  author?: string;
  content: string;
}): Promise<{ path: string }> {
  const res = await fetch(`${BASE}/api/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

export function createChatSocket(): WebSocket {
  const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return new WebSocket(`${wsProtocol}//${window.location.host}/api/chat`);
}
