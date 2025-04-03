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
          <DialogTitle>Edit Reference</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <label htmlFor="edit-url" className="text-sm font-bold">
            Reference URL
          </label>
          <Input
            id="edit-url"
            placeholder="Reference URL"
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
            Reference Title
          </label>
          <Input
            id="edit-title"
            placeholder="Reference Title"
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
            Reference Description
          </label>
          <Textarea
            id="edit-description"
            placeholder="Reference Description"
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
          Save Changes
        </Button>
      </DialogContent>
    </Dialog>
  );
}
