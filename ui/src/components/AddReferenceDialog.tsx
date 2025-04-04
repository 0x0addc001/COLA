import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { PlusCircle, Plus } from "lucide-react";
import { Reference } from "@/lib/types";

type AddReferenceDialogProps = {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  newReference: Reference;
  setNewReference: (reference: Reference) => void;
  addReference: () => void;
};

export function AddReferenceDialog({
  isOpen,
  onOpenChange,
  newReference,
  setNewReference,
  addReference,
}: AddReferenceDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogTrigger asChild>
        <Button
          variant="link"
          size="sm"
          className="text-sm font-bold text-[#6766FC]"
        >
          {/*Add References */}
          添加
          <PlusCircle className="w-6 h-6 ml-2" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Reference</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <label htmlFor="new-url" className="text-sm font-bold">
            Reference URL
          </label>
          <Input
            id="new-url"
            placeholder="Reference URL"
            value={newReference.url || ""}
            onChange={(e) =>
              setNewReference({ ...newReference, url: e.target.value })
            }
            aria-label="New reference URL"
            className="bg-background"
          />
          <label htmlFor="new-title" className="text-sm font-bold">
            Reference Title
          </label>
          <Input
            id="new-title"
            placeholder="Reference Title"
            value={newReference.title || ""}
            onChange={(e) =>
              setNewReference({ ...newReference, title: e.target.value })
            }
            aria-label="New reference title"
            className="bg-background"
          />
          <label htmlFor="new-description" className="text-sm font-bold">
            Reference Description
          </label>
          <Textarea
            id="new-description"
            placeholder="Reference Description"
            value={newReference.description || ""}
            onChange={(e) =>
              setNewReference({
                ...newReference,
                description: e.target.value,
              })
            }
            aria-label="New reference description"
            className="bg-background"
          />
        </div>
        <Button
          onClick={addReference}
          className="w-full bg-[#6766FC] text-white"
          disabled={
            !newReference.url || !newReference.title || !newReference.description
          }
        >
          <Plus className="w-4 h-4 mr-2" /> Add Reference
        </Button>
      </DialogContent>
    </Dialog>
  );
}
