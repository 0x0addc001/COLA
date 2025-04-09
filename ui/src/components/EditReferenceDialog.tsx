import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Reference } from "@/lib/types";

type EditResourceDialogProps = {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  editReference: Reference | null;
  setEditReference: (
    reference: ((prev: Reference | null) => Reference | null) | Reference | null
  ) => void;
  updateReference: () => void;
};

export function EditReferenceDialog({
  isOpen,
  onOpenChange,
  editReference,
  setEditReference,
  updateReference,
}: EditResourceDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>编辑参考资料</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <label htmlFor="edit-url" className="text-sm font-bold">
            参考资料URL
          </label>
          <Input
            id="edit-url"
            placeholder="参考资料URL"
            value={editReference?.url || ""}
            onChange={(e) =>
              setEditReference((prev) =>
                prev ? { ...prev, url: e.target.value } : null
              )
            }
            aria-label="Edit reference URL"
            className="bg-background"
          />
          <label htmlFor="edit-title" className="text-sm font-bold">
            参考资料标题
          </label>
          <Input
            id="edit-title"
            placeholder="参考资料标题"
            value={editReference?.title || ""}
            onChange={(e) =>
              setEditReference((prev: any) =>
                prev ? { ...prev, title: e.target.value } : null
              )
            }
            aria-label="Edit reference title"
            className="bg-background"
          />
          <label htmlFor="edit-description" className="text-sm font-bold">
            参考资料描述
          </label>
          <Textarea
            id="edit-description"
            placeholder="参考资料描述"
            value={editReference?.description || ""}
            onChange={(e) =>
              setEditReference((prev) =>
                prev ? { ...prev, description: e.target.value } : null
              )
            }
            aria-label="Edit reference description"
            className="bg-background"
          />
        </div>
        <Button
          onClick={updateReference}
          className="w-full bg-[#6766FC] text-white"
          disabled={
            !editReference?.url ||
            !editReference?.title ||
            !editReference?.description
          }
        >
          保存修改
        </Button>
      </DialogContent>
    </Dialog>
  );
}
