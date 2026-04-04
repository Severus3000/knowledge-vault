export interface VaultFile {
  name: string;
  path: string;
  dir: string;
}

export interface VaultTree {
  raw: VaultFile[];
  wiki: VaultFile[];
  outputs: VaultFile[];
}

export interface FileContent {
  content: string;
  frontmatter: Record<string, unknown>;
  body: string;
}

export interface SearchResult {
  path: string;
  title: string;
  snippet: string;
}

export interface VaultStats {
  raw_count: number;
  wiki_count: number;
  last_compiled: string;
}

export interface GraphData {
  nodes: { id: string; label: string }[];
  edges: { source: string; target: string }[];
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}
