"use client";

import React from "react";
import { createContext, useContext, useState, ReactNode } from "react";

type AgentSelectorContextType = {
  setAgent: (agent: string) => void;
  agent: string;
  lgcDeploymentUrl?: string | null;
  hidden: boolean;
  setHidden: (hidden: boolean) => void;
};

const AgentSelectorContext = createContext<
  AgentSelectorContextType | undefined
>(undefined);

export const AgentSelectorProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const agent =
    globalThis.window === undefined
      ? "modeler"
      : new URL(window.location.href).searchParams.get("agentType") ??
        "modeler";
  const [hidden, setHidden] = useState<boolean>(false);

  const setAgent = (agent: string) => {
    const url = new URL(window.location.href);
    url.searchParams.set("agentType", agent);
    window.location.href = url.toString();
  };

  const lgcDeploymentUrl =
    globalThis.window === undefined
      ? null
      : new URL(window.location.href).searchParams.get("lgcDeploymentUrl");

  return (
    <AgentSelectorContext.Provider
      value={{
        agent,
        lgcDeploymentUrl,
        hidden,
        setAgent,
        setHidden,
      }}
    >
      {children}
    </AgentSelectorContext.Provider>
  );
};

export const useAgentSelectorContext = () => {
  const context = useContext(AgentSelectorContext);
  if (context === undefined) {
    throw new Error(
      "useAgentSelectorContext must be used within an AgentSelectorProvider"
    );
  }
  return context;
};
