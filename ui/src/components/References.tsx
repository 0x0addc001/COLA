import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
import { Reference } from "@/lib/types";
import { truncateUrl } from "@/lib/utils";

type ReferencesProps = {
  references: Reference[];
  customWidth?: number;
  handleCardClick?: (reference: Reference) => void;
  removeReference?: (url: string) => void;
};

export function References({
  references,
  handleCardClick,
  removeReference,
  customWidth,
}: ReferencesProps) {
  return (
    <div data-test-id="references" className="flex space-x-3 overflow-x-auto">
      {references.map((reference, idx) => (
        <Card
          data-test-id={`reference`}
          key={idx}
          className={
            "bg-background border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 flex-none" +
            (handleCardClick ? " cursor-pointer" : "")
          }
          style={{ width: customWidth + "px" || "320px" }}
          onClick={() => handleCardClick?.(reference)}
        >
          <CardContent className="px-6 py-6 relative">
            <div className="flex items-start space-x-3 text-sm">
              <div className="flex-grow">
                <h3
                  className="font-bold text-lg"
                  style={{
                    maxWidth: customWidth ? customWidth - 30 + "px" : "230px",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {reference.title}
                </h3>
                <p
                  className="text-base mt-2"
                  style={{
                    maxWidth: customWidth ? customWidth - 30 + "px" : "250px",
                    overflowWrap: "break-word",
                  }}
                >
                  {reference.description?.length > 250
                    ? reference.description.slice(0, 250) + "..."
                    : reference.description}
                </p>
                <a
                  href={reference.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-primary hover:underline mt-3 text-slate-400 inline-block"
                  title={reference.url}
                  style={{
                    width: customWidth ? customWidth - 30 + "px" : "250px",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {reference.description && (
                    <>
                      <img
                        src={`https://www.google.com/s2/favicons?domain=${reference.url}`}
                        alt="favicon"
                        className="inline-block mr-2"
                        style={{ width: "16px", height: "16px" }}
                      />
                      {truncateUrl(reference.url)}
                    </>
                  )}
                </a>
              </div>
              {removeReference && (
                <div className="flex items-start absolute top-4 right-4">
                  <Button
                    data-test-id="remove-reference"
                    variant="ghost"
                    size="icon"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeReference?.(reference.url);
                    }}
                    aria-label={`Remove ${reference.url}`}
                  >
                    <Trash2 className="w-6 h-6 text-gray-400 hover:text-red-500" />
                  </Button>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
