import {
  CopilotRuntime,
  OpenAIAdapter,
  // langGraphPlatformEndpoint,
  copilotRuntimeNextJSAppRouterEndpoint,
  copilotKitEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

export const POST = async (req: NextRequest) => {

  // const searchParams = req.nextUrl.searchParams;
  // const deploymentUrl =
  //   searchParams.get("lgcDeploymentUrl") || process.env.LGC_DEPLOYMENT_URL;
  // const langsmithApiKey = process.env.LANGSMITH_API_KEY as string;

  const remoteEndpoint =
        // deploymentUrl?
        // langGraphPlatformEndpoint({
        //   deploymentUrl,
        //   langsmithApiKey,
        //   agents: [
        //     {
        //       name: "modeler",
        //       description: "Formulation Agent",
        //     },
        //     {
        //       name: "adapter",
        //       description: "Translation Agent",
        //     },
        //     {
        //       name: "renderer",
        //       description: "Visualization Agent",
        //     },
        //   ],
        // })
        // :
        copilotKitEndpoint({
          url:
            "http://localhost:8000/copilotkit",
        });

  const runtime = new CopilotRuntime({
    remoteEndpoints: [remoteEndpoint],
  });

  const llmAdapter = new OpenAIAdapter({})

  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime: runtime,
    serviceAdapter: llmAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
