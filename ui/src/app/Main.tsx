import { DesignCanvas } from "@/components/DesignCanvas";
import { useAgentSelectorContext } from "@/lib/agent-selector-provider";
import { AgentState } from "@/lib/types";
import { useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";

export default function Main() {
  const { agent } = useAgentSelectorContext();
  const { state, setState } = useCoAgent<AgentState>({
    name: agent,
    initialState: {
      logs: [],
      project_settings:
          "**设计理念：**  \n" +
          "以自然与可持续发展为核心，融合现代简约与传统元素，创造人与环境和谐共生的生活场景。\n" +
          "**功能用途：**  \n" +
          "提供休闲娱乐、社交聚会、艺术展示与文化体验的多功能公共空间。\n" +
          "**用户客群：**  \n" +
          "主要面向家庭、年轻白领、社区居民及城市游客。\n" +
          "**风格样式：**  \n" +
          "现代自然主义风格，融合东方园林的含蓄与西方景观的开放性，强调自然肌理与空间流动，采用几何与有机形态的结合，呈现简约、生态且富有艺术美感的视觉体验。" +
          "**感觉体验：**  \n" +
          "营造轻松愉悦、温馨自然且充满艺术气息的空间感受，让人仿佛置身于自然的怀抱中。\n" +
          "**用地面积：**  \n" +
          "约2000平方米。\n" +
          "**必要景观元素：**  \n" +
          "水景喷泉、步行小径、休息亭、雕塑装置、花坛及开阔草坪。\n" +
          "**材料偏好：**  \n" +
          "天然石材、环保木材、再生混凝土与玻璃元素。\n" +
          "**植物偏好：**  \n" +
          "本土树种、四季花卉、耐旱灌木与攀缘植物，注重季节性变化与色彩搭配。\n",
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
