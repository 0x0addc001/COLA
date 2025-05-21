import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { ImageInput } from "@/components/ui/imageinput";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { PlusCircle, Plus } from "lucide-react";
import { Image } from "@/lib/types";

type AddImageDialogProps = {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  newImage: Image;
  setNewImage: (image: Image) => void;
  addImage: () => void;
};

export function AddImageDialog({
  isOpen,
  onOpenChange,
  newImage,
  setNewImage,
  addImage,
}: AddImageDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogTrigger asChild>
        <Button
          variant="link"
          size="sm"
          className="text-sm font-bold text-[#6766FC]"
        >
          {/*Add Images */}
          添加
          <PlusCircle className="w-6 h-6 ml-2" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>添加新的参考图</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <label htmlFor="new-url" className="text-sm font-bold">
            参考图URL
          </label>

          {/*模仿此处的代码示例，修改新的上传组件的代码*/}
          {/*<Input*/}
          {/*  id="new-url"*/}
          {/*  placeholder="参考图URL"*/}
          {/*  value={newImage.url || ""}*/}
          {/*  onChange={(e) =>*/}
          {/*    setNewImage({ ...newImage, url: e.target.value })*/}
          {/*  }*/}
          {/*  aria-label="New image URL"*/}
          {/*  className="bg-background"*/}
          {/*/>*/}
          {/* 使用 ImageInput 代替 Input 手动输入 URL */}
          <ImageInput
            className="bg-background"
            onUploadSuccess={(url) =>
              setNewImage({ ...newImage, url })
            }
          />
          {newImage.url && (
            <img
              src={newImage.url}
              alt="上传图片预览"
              className="mt-4 max-w-xs border rounded"
            />
          )}

          {/*<label htmlFor="new-instruction" className="text-sm font-bold">*/}
          {/*  参考指令*/}
          {/*</label>*/}
          {/*<Input*/}
          {/*  id="new-instruction"*/}
          {/*  placeholder="参考指令"*/}
          {/*  value={newImage.instruction || ""}*/}
          {/*  onChange={(e) =>*/}
          {/*    setNewImage({ ...newImage, instruction: e.target.value })*/}
          {/*  }*/}
          {/*  aria-label="New image instruction"*/}
          {/*  className="bg-background"*/}
          {/*/>*/}
        </div>
        <Button
          onClick={addImage}
          className="w-full bg-[#6766FC] text-white"
          disabled={
            !newImage.url
            // || !newImage.instruction
          }
        >
          <Plus className="w-4 h-4 mr-2" /> 添加参考图
        </Button>
      </DialogContent>
    </Dialog>
  );
}
