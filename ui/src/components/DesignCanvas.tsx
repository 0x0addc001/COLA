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


  // img_references
  const img_references: Reference[] = state.img_references || [];

  useCopilotAction({ // Human-in-the-loop delete image references
    name: "DeleteImgReferences",
    description:
      "Prompt the user for image reference delete confirmation, and then perform image reference deletion",
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
          data-test-id="delete-image-reference-generative-ui-container"
        >
          <div className="font-bold text-base mb-2">
            Delete these image references?
          </div>
          <References
            references={img_references.filter((reference) =>
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

  const setImgReferences = (img_references: Reference[]) => {
    setState({ ...state, img_references });
  };

  // const [references, setReferences] = useState<Reference[]>(dummyReferences);
  const [newImgReference, setNewImgReference] = useState<Reference>({
    url: "",
    title: "",
    description: "",
  });
  const [isAddImgReferenceOpen, setIsAddImgReferenceOpen] = useState(false);

  const addImgReference = () => {
    if (newImgReference.url) {
      setImgReferences([...img_references, { ...newImgReference }]);
      setNewImgReference({ url: "", title: "", description: "" });
      setIsAddImgReferenceOpen(false);
    }
  };

  const removeImgReference = (url: string) => {
    setImgReferences(
      img_references.filter((img_reference: Reference) => img_reference.url !== url)
    );
  };

  const [editImgReference, setEditImgReference] = useState<Reference | null>(null);
  const [originalImgRefUrl, setOriginalImgRefUrl] = useState<string | null>(null);
  const [isEditImgReferenceOpen, setIsEditImgReferenceOpen] = useState(false);

  const handleCardClick_imgRef = (img_reference: Reference) => {
    setEditImgReference({ ...img_reference }); // Ensure a new object is created
    setOriginalImgRefUrl(img_reference.url); // Store the original URL
    setIsEditImgReferenceOpen(true);
  };

  const updateImgReference = () => {
    if (editImgReference && originalImgRefUrl) {
      setImgReferences(
        img_references.map((img_reference) =>
          img_reference.url === originalImgRefUrl ? { ...editImgReference } : img_reference
        )
      );
      setEditImgReference(null);
      setOriginalImgRefUrl(null);
      setIsEditImgReferenceOpen(false);
    }
  };

  // prototype_imgs
  const prototype_imgs: Reference[] = state.prototype_imgs || [];

  useCopilotAction({ // Human-in-the-loop delete prototype images
    name: "DeletePrototypeImgs",
    description:
      "Prompt the user for prototype images delete confirmation, and then perform prototype image deletion",
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
          data-test-id="delete-prototype-image-generative-ui-container"
        >
          <div className="font-bold text-base mb-2">
            Delete these prototype image?
          </div>
          <References
            references={prototype_imgs.filter((prototype_img) =>
              (args.urls || []).includes(prototype_img.url)
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

  const setPrototypeImgs = (prototype_imgs: Reference[]) => {
    setState({ ...state, prototype_imgs });
  };

  // const [references, setReferences] = useState<Reference[]>(dummyReferences);
  const [newPrototypeImg, setNewPrototypeImg] = useState<Reference>({
    url: "",
    title: "",
    description: "",
  });
  const [isAddPrototypeImgOpen, setIsAddPrototypeImgOpen] = useState(false);

  const addPrototypeImg = () => {
    if (newPrototypeImg.url) {
      setPrototypeImgs([...prototype_imgs, { ...newPrototypeImg }]);
      setNewPrototypeImg({ url: "", title: "", description: "" });
      setIsAddPrototypeImgOpen(false);
    }
  };

  const removePrototypeImg = (url: string) => {
    setPrototypeImgs(
      prototype_imgs.filter((reference: Reference) => reference.url !== url)
    );
  };

  const [editPrototypeImg, setEditPrototypeImg] = useState<Reference | null>(null);
  const [originalProtoypeImgUrl, setOriginalProtoypeImgUrl] = useState<string | null>(null);
  const [isEditPrototypeImgOpen, setIsEditPrototypeImgOpen] = useState(false);

  const handleCardClick_prototypeImg = (prototype_img: Reference) => {
    setEditPrototypeImg({ ...prototype_img }); // Ensure a new object is created
    setOriginalProtoypeImgUrl(prototype_img.url); // Store the original URL
    setIsEditPrototypeImgOpen(true);
  };

  const updatePrototypeImg = () => {
    if (editPrototypeImg && originalProtoypeImgUrl) {
      setPrototypeImgs(
        prototype_imgs.map((prototype_img) =>
          prototype_img.url === originalProtoypeImgUrl ? { ...editPrototypeImg } : prototype_img
        )
      );
      setEditPrototypeImg(null);
      setOriginalProtoypeImgUrl(null);
      setIsEditPrototypeImgOpen(false);
    }
  };

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
              // "设计理念：\n功能用途：\n用户客群：\n感觉体验：\n用地面积：\n必要景观元素：\n材料偏好：\n植物偏好：\n"
            value={state.project_settings ||
                "【设计理念】\n" +
                "\"未来生态绿洲\" - 通过数字化自然模拟技术实现人与生态系统的智能互动，将生物多样性保护、碳中和功能与沉浸式感官体验相结合，打造具有自我修复能力的科技型生态景观。\n" +
                "【功能用途】\n" +
                "• 城市生态海绵体（雨水渗透率≥85%）\n" +
                "• 沉浸式自然教育中心\n" +
                "• 模块化户外办公空间\n" +
                "• 智慧健身环道（配备运动数据采集）\n" +
                "• 夜间星空观测平台\n" +
                "• 城市农业示范区\n" +
                "【用户客群】\n" +
                "• 25-45岁科技从业者（占比40%）\n" +
                "• 生态敏感型家庭（占比30%）\n" +
                "• 城市自然疗愈需求者（占比20%）\n" +
                "• 研学教育机构（占比10%）\n" +
                "【感觉体验】\n" +
                "视觉：动态光谱照明（模拟日出到极光变化）\n" +
                "听觉：声景矩阵（分区播放雨林/草原/湿地白噪音）\n" +
                "触觉：智能材质交互地面（随脚步改变温度/质感）\n" +
                "嗅觉：芳香植物释放系统（定时雾化不同植物精油）\n" +
                "味觉：可食用景观带（莓果走廊/香草迷宫）\n" +
                "【用地面积】\n" +
                "12万平方米（L形地块，长边800m，短边150m，包含6米高差）\n" +
                "【必要景观元素】\n" +
                "• 生物沟壑系统（兼具排水与生态廊道功能）\n" +
                "• 碳捕捉绿塔（垂直种植+空气净化装置）\n" +
                "• AR互动景墙（显示实时生态数据）\n" +
                "• 仿生蜂巢休憩亭（3D打印生物基材料）\n" +
                "• 智慧年轮广场（同心圆铺装记录碳排放数据）\n" +
                "• 荧光菌丝网络（地下真菌共生系统可视化）\n" +
                "【材料偏好】\n" +
                "• 结构材料：再生铝合金、自修复生物混凝土\n" +
                "• 铺装材料：光催化透水砖、碳化竹木复合板\n" +
                "• 装饰材料：回收玻璃骨料、磁流体艺术装置\n" +
                "• 智能材料：光伏薄膜、压电发电地砖\n" +
                "• 水景材料：生态固化剂处理的天然粘土\n" +
                "【植物偏好】\n" +
                "• 冠层：杂交马褂木（Liriodendron tulipifera 'Solaris'）\n" +
                "• 中层：量子点标记型红枫（Acer × freemanii 'Dataflow'）\n" +
                "• 地被：耐践踏生态草坪（Zoysia matrella 'EcoWalk'）\n" +
                "• 特色品种：\n" +
                "空气凤梨矩阵（Tillandsia cyberneticus）\n" +
                "荧光蕨类墙（Cyathea illuminata）\n" +
                "食用景观带（杂交蓝莓'InfinityBerry'） • 生态功能组合： 雨水花园区：梭鱼草+旱伞草+花叶芦竹 固碳优先区：中山杉+木荷+海桐球"}
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
              isOpen={isEditImgReferenceOpen}
              onOpenChange={setIsEditImgReferenceOpen}
              editReference={editImgReference}
              setEditReference={setEditImgReference}
              updateReference={updateImgReference}
            />
            <AddReferenceDialog
              isOpen={isAddImgReferenceOpen}
              onOpenChange={setIsAddImgReferenceOpen}
              newReference={newImgReference}
              setNewReference={setNewImgReference}
              addReference={addImgReference}
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
              handleCardClick={handleCardClick_imgRef}
              removeReference={removeImgReference}
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
              isOpen={isEditPrototypeImgOpen}
              onOpenChange={setIsEditPrototypeImgOpen}
              editReference={editPrototypeImg}
              setEditReference={setEditPrototypeImg}
              updateReference={updatePrototypeImg}
            />
            <AddReferenceDialog
              isOpen={isAddPrototypeImgOpen}
              onOpenChange={setIsAddPrototypeImgOpen}
              newReference={newPrototypeImg}
              setNewReference={setNewPrototypeImg}
              addReference={addPrototypeImg}
            />
          </div>
          {prototype_imgs.length !== 0 && (
            <References
              references={prototype_imgs}
              handleCardClick={handleCardClick_prototypeImg}
              removeReference={removePrototypeImg}
            />
          )}
        </div>

      </div>
    </div>
  );
}
