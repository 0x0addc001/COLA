import { DesignCanvas } from "@/components/DesignCanvas";
import { useAgentSelectorContext } from "@/lib/agent-selector-provider";
import { AgentState } from "@/lib/types";
import { useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";

export default function Main() {
  const { agent } = useAgentSelectorContext();
  // useState -> React
  // useCoAgent -> CopilotKit
  const { state, setState } = useCoAgent<AgentState>({ // Sync the state across the ui-form and the agent!!!
    name: agent,
    initialState: {
      logs: [],
      project_settings: "",
      references: [],
      design_plan: "",
      plan2img_prompt:  "",
      img_references: [],
      prototype_imgs: [],
    },
  });

  useCopilotChatSuggestions({
    instructions: "Test🥤",
  });

  return (
    <>
      <h1 className="flex h-[60px] bg-[#FFF] text-[#6766FC] items-center px-10 text-2xl font-medium">
        🥤COLA: COpilot for Landscape Architecture 景观设计助手
      </h1>

      <div
        className="flex flex-1 border"
        style={{ height: "calc(100vh - 60px)" }}
      >
        <div className="flex-1 overflow-hidden">
          <DesignCanvas />
        </div>
        <div
          className="w-[500px] h-full flex-shrink-0"
          style={
            {
              "--copilot-kit-background-color": "#E0E9FD",
              "--copilot-kit-separator-color": "#b8b8b8",

              "--copilot-kit-primary-color": "#FFF",
              "--copilot-kit-secondary-color": "#6766FC",

              "--copilot-kit-contrast-color": "#000",
              "--copilot-kit-secondary-contrast-color": "#000",
            } as any
          }
        >
          <CopilotChat
            className="h-full"
            onSubmitMessage={async (message) => {
              // clear the logs before starting the new research
              setState({ ...state, logs: [] });
              await new Promise((resolve) => setTimeout(resolve, 30));
            }}
            // "Hey, just tell me about your design!😊🥤"
            labels={{
              initial: "嘿，跟我说说你的设计吧！😊🥤",
            }}
          />
        </div>
      </div>
    </>
  );
}
