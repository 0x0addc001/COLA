import {Card, CardContent} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Trash2} from "lucide-react";
import {Image} from "@/lib/types";
import {truncateUrl} from "@/lib/utils";

type ImagesProps = {
    images: Image[],
    customWidth?: number,
    handleCardClick?: (image: Image) => void,
    removeImage?: (url: string) => void,
};

export function Images({
                               images,
                               handleCardClick,
                               removeImage,
                               customWidth,
                           }: ImagesProps) {
    return (
        <div data-test-id="images" className="flex space-x-3 overflow-x-auto">
            {images.map((image, idx) => (
                <Card
                    data-test-id={`image`}
                    key={idx}
                    className={
                        "bg-background border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 flex-none" +
                        (handleCardClick ? " cursor-pointer" : "")
                    }
                    style={{width: customWidth + "px" || "320px"}}
                    onClick={() => handleCardClick?.(image)}
                >
                    <CardContent className="px-6 py-6 relative">
                        <div className="flex items-start space-x-3 text-sm">
                            <div className="flex-grow">
                                <img
                                    src={image.url}
                                    alt="favicon"
                                    className="inline-block mr-2"
                                    style={{width: "1024px", height: "1024px"}}
                                />
                            </div>
                            {removeImage && (
                                <div className="flex items-start absolute top-4 right-4">
                                    <Button
                                        data-test-id="remove-image"
                                        variant="ghost"
                                        size="icon"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            removeImage?.(image.url);
                                        }}
                                        aria-label={`Remove ${image.url}`}
                                    >
                                        <Trash2 className="w-6 h-6 text-gray-400 hover:text-red-500"/>
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