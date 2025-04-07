export type Reference = {
  url: string;
  title: string;
  description: string;
};

export type AgentState = {
  logs: any[];
  project_settings: string;
  references: any[];
  design_plan: string;
  plan2img_prompt: string;
  img_references: any[];
  prototype_imgs: any[];
}