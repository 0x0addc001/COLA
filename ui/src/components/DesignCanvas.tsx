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

  const references: Reference[] = state.references || [];
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

  return (
    <div className="w-full h-full overflow-y-auto p-10 bg-[#F5F8FF]">
      <div className="space-y-8 pb-10">
        <div>
          <h2 className="text-lg font-medium mb-3 text-primary">
            Project Settings
          </h2>
          {/*<Input*/}
          {/*  // placeholder="Enter your project settings"*/}
          {/*  value={state.project_settings || ""}*/}
          {/*  onChange={(e) =>*/}
          {/*    setState({ ...state, project_settings: e.target.value })*/}
          {/*  }*/}
          {/*  aria-label="Project settings"*/}
          {/*  className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"*/}
          {/*  style={{ minHeight: "200px" }}*/}
          {/*/>*/}
          <Textarea
            // placeholder="Enter your project settings"
            value={state.project_settings || ""}
            onChange={(e) =>
              setState({ ...state, project_settings: e.target.value })
            }
            aria-label="Project settings"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
            style={{ minHeight: "200px" }}
          />
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-primary">Plan References</h2>
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
              Click the button above to add references.
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
            Design Plan
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
            Plan2Image Prompt
          </h2>
          <Textarea
            data-test-id="plan2img-prompt"
            // placeholder="Write your research draft here"
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
            <h2 className="text-lg font-medium text-primary">Image References</h2>
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
              Click the button above to add references.
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
            Prototype Image
          </h2>
          <Textarea
            data-test-id="prototype-image"
            // placeholder="Write your research draft here"
            value={state.prototype_img || ""}
            onChange={(e) => setState({ ...state, prototype_img: e.target.value })}
            rows={10}
            aria-label="Research draft"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
            style={{ minHeight: "200px" }}
          />
        </div>

      </div>
    </div>
  );
}
