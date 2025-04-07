"use client";

import React from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useAgentSelectorContext } from "@/lib/agent-selector-provider";

export function AgentSelector() {
  const { agent, setAgent } = useAgentSelectorContext();

  return (
    <div className="fixed top-0 right-0 p-4 z-50">
      <Select value={agent} onValueChange={(v) => setAgent(v)}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Theme" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="cola">项目1</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
