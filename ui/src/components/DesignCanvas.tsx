"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  useCoAgent,
  useCoAgentStateRender,
  useCopilotAction,
} from "@copilotkit/react-core";
import { Progress } from "./Progress";
import { EditReferenceDialog } from "./EditReferenceDialog";
import { AddReferenceDialog } from "./AddReferenceDialog";
import { References } from "./References";
import { AgentState, Reference } from "@/lib/types";
import { useAgentSelectorContext } from "@/lib/agent-selector-provider";

export function DesignCanvas() {
  const { agent } = useAgentSelectorContext();

  const { state, setState } = useCoAgent<AgentState>({
    name: agent,
    initialState: {
    },
  });

  useCoAgentStateRender({ // Render progress
    name: agent,
    render: ({ state, nodeName, status }) => {
      if (!state.logs || state.logs.length === 0) {
        return null;
      }
      return <Progress logs={state.logs} />;
    },
  });

  // references
  const references: Reference[] = state.references || [];

  useCopilotAction({ // Human-in-the-loop delete references
    name: "DeleteReferences",
    description:
      "Prompt the user for reference delete confirmation, and then perform reference deletion",
    available: "remote",
    parameters: [
      {
        name: "urls",
        type: "string[]",
      },
    ],
    renderAndWait: ({ args, status, handler }) => {
      return (
        <div
          className=""
          data-test-id="delete-reference-generative-ui-container"
        >
          <div className="font-bold text-base mb-2">
            Delete these references?
          </div>
          <References
            references={references.filter((reference) =>
              (args.urls || []).includes(reference.url)
            )}
            customWidth={200}
          />
          {status === "executing" && (
            <div className="mt-4 flex justify-start space-x-2">
              <button
                onClick={() => handler("NO")}
                className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
              >
                Cancel
              </button>
              <button
                data-test-id="button-delete"
                onClick={() => handler("YES")}
                className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
              >
                Delete
              </button>
            </div>
          )}
        </div>
      );
    },
  });

  const setReferences = (references: Reference[]) => {
    setState({ ...state, references });
  };

  // const [references, setReferences] = useState<Reference[]>(dummyReferences);
  const [newReference, setNewReference] = useState<Reference>({
    url: "",
    title: "",
    description: "",
  });
  const [isAddReferenceOpen, setIsAddReferenceOpen] = useState(false);

  const addReference = () => {
    if (newReference.url) {
      setReferences([...references, { ...newReference }]);
      setNewReference({ url: "", title: "", description: "" });
      setIsAddReferenceOpen(false);
    }
  };

  const removeReference = (url: string) => {
    setReferences(
      references.filter((reference: Reference) => reference.url !== url)
    );
  };

  const [editReference, setEditReference] = useState<Reference | null>(null);
  const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  const [isEditReferenceOpen, setIsEditReferenceOpen] = useState(false);

  const handleCardClick = (reference: Reference) => {
    setEditReference({ ...reference }); // Ensure a new object is created
    setOriginalUrl(reference.url); // Store the original URL
    setIsEditReferenceOpen(true);
  };

  const updateReference = () => {
    if (editReference && originalUrl) {
      setReferences(
        references.map((reference) =>
          reference.url === originalUrl ? { ...editReference } : reference
        )
      );
      setEditReference(null);
      setOriginalUrl(null);
      setIsEditReferenceOpen(false);
    }
  };


  // // img_references
  // const img_references: Reference[] = state.img_references || [];
  //
  // // Add
  // useCopilotAction({ // Human-in-the-loop delete references
  //   name: "DeleteReferences",
  //   description:
  //     "Prompt the user for reference delete confirmation, and then perform reference deletion",
  //   available: "remote",
  //   parameters: [
  //     {
  //       name: "urls",
  //       type: "string[]",
  //     },
  //   ],
  //   renderAndWait: ({ args, status, handler }) => {
  //     return (
  //       <div
  //         className=""
  //         data-test-id="delete-reference-generative-ui-container"
  //       >
  //         <div className="font-bold text-base mb-2">
  //           Delete these references?
  //         </div>
  //         <References
  //           references={references.filter((reference) =>
  //             (args.urls || []).includes(reference.url)
  //           )}
  //           customWidth={200}
  //         />
  //         {status === "executing" && (
  //           <div className="mt-4 flex justify-start space-x-2">
  //             <button
  //               onClick={() => handler("NO")}
  //               className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
  //             >
  //               Cancel
  //             </button>
  //             <button
  //               data-test-id="button-delete"
  //               onClick={() => handler("YES")}
  //               className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
  //             >
  //               Delete
  //             </button>
  //           </div>
  //         )}
  //       </div>
  //     );
  //   },
  // });
  //
  // const setReferences = (references: Reference[]) => {
  //   setState({ ...state, references });
  // };
  //
  // // const [references, setReferences] = useState<Reference[]>(dummyReferences);
  // const [newReference, setNewReference] = useState<Reference>({
  //   url: "",
  //   title: "",
  //   description: "",
  // });
  // const [isAddReferenceOpen, setIsAddReferenceOpen] = useState(false);
  //
  // const addReference = () => {
  //   if (newReference.url) {
  //     setReferences([...references, { ...newReference }]);
  //     setNewReference({ url: "", title: "", description: "" });
  //     setIsAddReferenceOpen(false);
  //   }
  // };
  //
  // const removeReference = (url: string) => {
  //   setReferences(
  //     references.filter((reference: Reference) => reference.url !== url)
  //   );
  // };
  //
  // const [editReference, setEditReference] = useState<Reference | null>(null);
  // const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  // const [isEditReferenceOpen, setIsEditReferenceOpen] = useState(false);
  //
  // const handleCardClick = (reference: Reference) => {
  //   setEditReference({ ...reference }); // Ensure a new object is created
  //   setOriginalUrl(reference.url); // Store the original URL
  //   setIsEditReferenceOpen(true);
  // };
  //
  // const updateReference = () => {
  //   if (editReference && originalUrl) {
  //     setReferences(
  //       references.map((reference) =>
  //         reference.url === originalUrl ? { ...editReference } : reference
  //       )
  //     );
  //     setEditReference(null);
  //     setOriginalUrl(null);
  //     setIsEditReferenceOpen(false);
  //   }
  // };

  // // prototype_imgs
  // const prototype_imgs: Reference[] = state.prototype_imgs || [];
  //
  // // Add
  // useCopilotAction({ // Human-in-the-loop delete references
  //   name: "DeleteReferences",
  //   description:
  //     "Prompt the user for reference delete confirmation, and then perform reference deletion",
  //   available: "remote",
  //   parameters: [
  //     {
  //       name: "urls",
  //       type: "string[]",
  //     },
  //   ],
  //   renderAndWait: ({ args, status, handler }) => {
  //     return (
  //       <div
  //         className=""
  //         data-test-id="delete-reference-generative-ui-container"
  //       >
  //         <div className="font-bold text-base mb-2">
  //           Delete these references?
  //         </div>
  //         <References
  //           references={references.filter((reference) =>
  //             (args.urls || []).includes(reference.url)
  //           )}
  //           customWidth={200}
  //         />
  //         {status === "executing" && (
  //           <div className="mt-4 flex justify-start space-x-2">
  //             <button
  //               onClick={() => handler("NO")}
  //               className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
  //             >
  //               Cancel
  //             </button>
  //             <button
  //               data-test-id="button-delete"
  //               onClick={() => handler("YES")}
  //               className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
  //             >
  //               Delete
  //             </button>
  //           </div>
  //         )}
  //       </div>
  //     );
  //   },
  // });
  //
  // const setReferences = (references: Reference[]) => {
  //   setState({ ...state, references });
  // };
  //
  // // const [references, setReferences] = useState<Reference[]>(dummyReferences);
  // const [newReference, setNewReference] = useState<Reference>({
  //   url: "",
  //   title: "",
  //   description: "",
  // });
  // const [isAddReferenceOpen, setIsAddReferenceOpen] = useState(false);
  //
  // const addReference = () => {
  //   if (newReference.url) {
  //     setReferences([...references, { ...newReference }]);
  //     setNewReference({ url: "", title: "", description: "" });
  //     setIsAddReferenceOpen(false);
  //   }
  // };
  //
  // const removeReference = (url: string) => {
  //   setReferences(
  //     references.filter((reference: Reference) => reference.url !== url)
  //   );
  // };
  //
  // const [editReference, setEditReference] = useState<Reference | null>(null);
  // const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  // const [isEditReferenceOpen, setIsEditReferenceOpen] = useState(false);
  //
  // const handleCardClick = (reference: Reference) => {
  //   setEditReference({ ...reference }); // Ensure a new object is created
  //   setOriginalUrl(reference.url); // Store the original URL
  //   setIsEditReferenceOpen(true);
  // };
  //
  // const updateReference = () => {
  //   if (editReference && originalUrl) {
  //     setReferences(
  //       references.map((reference) =>
  //         reference.url === originalUrl ? { ...editReference } : reference
  //       )
  //     );
  //     setEditReference(null);
  //     setOriginalUrl(null);
  //     setIsEditReferenceOpen(false);
  //   }
  // };

  return (
    <div className="w-full h-full overflow-y-auto p-10 bg-[#F5F8FF]">
      <div className="space-y-8 pb-10">
        {/*<div>*/}
        {/*  <h2 className="text-lg font-medium mb-3 text-primary">*/}
        {/*    /!*Project Settings*!/*/}
        {/*    项目设定*/}
        {/*  </h2>*/}
        {/*  <Textarea*/}
        {/*    // placeholder="Enter your project settings"*/}
        {/*      // "Design Concept:\nFunctional Use:\nUser Profile:\nDesign Style:\nSensory Experience:\nLand Area:\nNecessary Landscape Elements:\nMaterial Preferences:\nPlant Preferences:\n"*/}
        {/*    value={state.project_settings || "设计理念：\n功能用途：\n用户客群：\n感觉体验：\n用地面积：\n必要景观元素：\n材料偏好：\n植物偏好：\n"}*/}
        {/*    onChange={(e) =>*/}
        {/*      setState({ ...state, project_settings: e.target.value })*/}
        {/*    }*/}
        {/*    aria-label="Project settings"*/}
        {/*    className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"*/}
        {/*    style={{ minHeight: "200px" }}*/}
        {/*  />*/}
        {/*</div>*/}

        <div className="flex flex-col h-full">
          <h2 className="text-lg font-medium mb-3 text-primary">
            {/*Project Settings*/}
            项目设定
          </h2>
          <Textarea
            data-test-id="project_settings"
            // placeholder="Write your project settings here"
            value={state.project_settings || "设计理念：\n功能用途：\n用户客群：\n感觉体验：\n用地面积：\n必要景观元素：\n材料偏好：\n植物偏好：\n"}
            onChange={(e) => setState({ ...state, project_settings: e.target.value })}
            rows={10}
            aria-label="Project settings"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
            style={{ minHeight: "200px" }}
          />
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-primary">
              {/*Plan References*/}
              参考资料
            </h2>
            <EditReferenceDialog
              isOpen={isEditReferenceOpen}
              onOpenChange={setIsEditReferenceOpen}
              editReference={editReference}
              setEditReference={setEditReference}
              updateReference={updateReference}
            />
            <AddReferenceDialog
              isOpen={isAddReferenceOpen}
              onOpenChange={setIsAddReferenceOpen}
              newReference={newReference}
              setNewReference={setNewReference}
              addReference={addReference}
            />
          </div>
          {references.length === 0 && (
            <div className="text-sm text-slate-400">
              {/*Click the button above to add references.*/}
              点击上方按钮添加参考资料
            </div>
          )}
          {references.length !== 0 && (
            <References
              references={references}
              handleCardClick={handleCardClick}
              removeReference={removeReference}
            />
          )}
        </div>

        <div className="flex flex-col h-full">
          <h2 className="text-lg font-medium mb-3 text-primary">
            {/*Design Plan*/}
            设计方案
          </h2>
          <Textarea
            data-test-id="design-plan"
            // placeholder="Write your design plan here"
            value={state.design_plan || ""}
            onChange={(e) => setState({ ...state, design_plan: e.target.value })}
            rows={10}
            aria-label="Design plan"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
            style={{ minHeight: "200px" }}
          />
        </div>

        <div className="flex flex-col h-full">
          <h2 className="text-lg font-medium mb-3 text-primary">
            {/*Plan2Image Prompt*/}
            Plan2Image 提示词
          </h2>
          <Textarea
            data-test-id="plan2img-prompt"
            // placeholder="Write your plan2img prompt here"
            value={state.plan2img_prompt || ""}
            onChange={(e) => setState({ ...state, plan2img_prompt: e.target.value })}
            rows={10}
            aria-label="Plan2Image prompt"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
            style={{ minHeight: "200px" }}
          />
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-primary">
              {/*Image References*/}
              参考图
            </h2>
            <EditReferenceDialog
              isOpen={isEditReferenceOpen}
              onOpenChange={setIsEditReferenceOpen}
              editReference={editReference}
              setEditReference={setEditReference}
              updateReference={updateReference}
            />
            <AddReferenceDialog
              isOpen={isAddReferenceOpen}
              onOpenChange={setIsAddReferenceOpen}
              newReference={newReference}
              setNewReference={setNewReference}
              addReference={addReference}
            />
          </div>
          {img_references.length === 0 && (
            <div className="text-sm text-slate-400">
              {/*Click the button above to add references.*/}
              点击上方按钮添加参考图
            </div>
          )}
          {img_references.length !== 0 && (
            <References
              references={img_references}
              handleCardClick={handleCardClick}
              removeReference={removeReference}
            />
          )}
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-primary">
              {/*Prototype Images*/}
              原型图
            </h2>
            <EditReferenceDialog
              isOpen={isEditReferenceOpen}
              onOpenChange={setIsEditReferenceOpen}
              editReference={editReference}
              setEditReference={setEditReference}
              updateReference={updateReference}
            />
            <AddReferenceDialog
              isOpen={isAddReferenceOpen}
              onOpenChange={setIsAddReferenceOpen}
              newReference={newReference}
              setNewReference={setNewReference}
              addReference={addReference}
            />
          </div>
          {prototype_imgs.length !== 0 && (
            <References
              references={prototype_imgs}
              handleCardClick={handleCardClick}
              removeReference={removeReference}
            />
          )}
        </div>

      </div>
    </div>
  );
}
