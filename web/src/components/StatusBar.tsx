import { useEffect, useState } from "react";
import { fetchStats } from "../api";
import type { VaultStats } from "../types";

export function StatusBar() {
  const [stats, setStats] = useState<VaultStats | null>(null);

  useEffect(() => {
    fetchStats().then(setStats).catch(console.error);
    const interval = setInterval(() => {
      fetchStats().then(setStats).catch(console.error);
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  if (!stats) return <div className="status-bar">Loading...</div>;

  return (
    <div className="status-bar">
      <span>{stats.raw_count} sources</span>
      <span>{stats.wiki_count} articles</span>
      <span>Last compiled: {stats.last_compiled}</span>
    </div>
  );
}
