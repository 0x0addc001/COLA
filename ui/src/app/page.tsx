"use client";

import { CopilotKit } from "@copilotkit/react-core";
import Main from "./Main";
import {
  AgentSelectorProvider,
  useAgentSelectorContext,
} from "@/lib/agent-selector-provider";
import { AgentSelector } from "@/components/AgentSelector";

export default function ModelSelectorWrapper() {
  return (
    <AgentSelectorProvider>
      <Home />
      <AgentSelector />
    </AgentSelectorProvider>
  );
}

function Home() {
  const { agent, lgcDeploymentUrl } = useAgentSelectorContext();

  // This logic is implemented to demonstrate multi-agent frameworks in this demo project.
  // There are cleaner ways to handle this in a production environment.
  const runtimeUrl = lgcDeploymentUrl
    ? `/api/copilotkit?lgcDeploymentUrl=${lgcDeploymentUrl}`
    : `/api/copilotkit`;

  return (
    <CopilotKit runtimeUrl={runtimeUrl} showDevConsole={false} agent={agent}>
      <Main />
    </CopilotKit>
  );
}
