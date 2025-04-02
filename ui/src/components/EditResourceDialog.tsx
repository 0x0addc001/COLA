import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Resource } from "@/lib/types";

type EditResourceDialogProps = {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  editResource: Resource | null;
  setEditResource: (
    resource: ((prev: Resource | null) => Resource | null) | Resource | null
  ) => void;
  updateResource: () => void;
};

export function EditResourceDialog({
  isOpen,
  onOpenChange,
  editResource,
  setEditResource,
  updateResource,
}: EditResourceDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit PlanReference</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <label htmlFor="edit-url" className="text-sm font-bold">
            PlanReference URL
          </label>
          <Input
            id="edit-url"
            placeholder="PlanReference URL"
            value={editResource?.url || ""}
            onChange={(e) =>
              setEditResource((prev) =>
                prev ? { ...prev, url: e.target.value } : null
              )
            }
            aria-label="Edit resource URL"
            className="bg-background"
          />
          <label htmlFor="edit-title" className="text-sm font-bold">
            PlanReference Title
          </label>
          <Input
            id="edit-title"
            placeholder="PlanReference Title"
            value={editResource?.title || ""}
            onChange={(e) =>
              setEditResource((prev: any) =>
                prev ? { ...prev, title: e.target.value } : null
              )
            }
            aria-label="Edit resource title"
            className="bg-background"
          />
          <label htmlFor="edit-description" className="text-sm font-bold">
            PlanReference Description
          </label>
          <Textarea
            id="edit-description"
            placeholder="PlanReference Description"
            value={editResource?.description || ""}
            onChange={(e) =>
              setEditResource((prev) =>
                prev ? { ...prev, description: e.target.value } : null
              )
            }
            aria-label="Edit resource description"
            className="bg-background"
          />
        </div>
        <Button
          onClick={updateResource}
          className="w-full bg-[#6766FC] text-white"
          disabled={
            !editResource?.url ||
            !editResource?.title ||
            !editResource?.description
          }
        >
          Save Changes
        </Button>
      </DialogContent>
    </Dialog>
  );
}
