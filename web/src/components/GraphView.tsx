import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { fetchGraph } from "../api";
import type { GraphData } from "../types";

interface GraphViewProps {
  onNodeClick: (path: string) => void;
}

export function GraphView({ onNodeClick }: GraphViewProps) {
  const [graph, setGraph] = useState<GraphData | null>(null);

  useEffect(() => {
    fetchGraph().then(setGraph).catch(console.error);
  }, []);

  if (!graph || graph.nodes.length === 0) {
    return (
      <div style={{ padding: 24, color: "#9ca3af", textAlign: "center" }}>
        No graph data yet. Ingest some content and run the compiler.
      </div>
    );
  }

  const graphData = {
    nodes: graph.nodes.map((n) => ({ id: n.id, name: n.label })),
    links: graph.edges.map((e) => ({ source: e.source, target: e.target })),
  };

  return (
    <ForceGraph2D
      graphData={graphData}
      nodeLabel="name"
      nodeColor={() => "#2563eb"}
      linkColor={() => "#d1d5db"}
      onNodeClick={(node) => onNodeClick(node.id as string)}
      width={240}
      height={300}
    />
  );
}
