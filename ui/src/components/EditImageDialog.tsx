import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Image } from "@/lib/types";

type EditResourceDialogProps = {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  editImage: Image | null;
  setEditImage: (
    image: ((prev: Image | null) => Image | null) | Image | null
  ) => void;
  updateImage: () => void;
};

export function EditImageDialog({
  isOpen,
  onOpenChange,
  editImage,
  setEditImage,
  updateImage,
}: EditResourceDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit Image</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <label htmlFor="edit-url" className="text-sm font-bold">
            Image URL
          </label>
          <Input
            id="edit-url"
            placeholder="Image URL"
            value={editImage?.url || ""}
            onChange={(e) =>
              setEditImage((prev) =>
                prev ? { ...prev, url: e.target.value } : null
              )
            }
            aria-label="Edit image URL"
            className="bg-background"
          />
          <label htmlFor="edit-instruction" className="text-sm font-bold">
            Image Title
          </label>
          <Input
            id="edit-instruction"
            placeholder="Image Title"
            value={editImage?.instruction || ""}
            onChange={(e) =>
              setEditImage((prev: any) =>
                prev ? { ...prev, instruction: e.target.value } : null
              )
            }
            aria-label="Edit image instruction"
            className="bg-background"
          />
        </div>
        <Button
          onClick={updateImage}
          className="w-full bg-[#6766FC] text-white"
          disabled={
            !editImage?.url ||
            !editImage?.instruction
          }
        >
          Save Changes
        </Button>
      </DialogContent>
    </Dialog>
  );
}
