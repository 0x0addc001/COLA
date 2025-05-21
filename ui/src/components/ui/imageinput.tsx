// imageinput.tsx
import * as React from "react"
import COS from "cos-js-sdk-v5"
import { Input } from "./input"

type ImageInputProps = {
  onUploadSuccess?: (url: string) => void
  className?: string
}

export const ImageInput = React.forwardRef<HTMLInputElement, ImageInputProps>(
  ({ onUploadSuccess, className, ...props }, ref) => {
    const [uploading, setUploading] = React.useState(false)
    const [progress, setProgress] = React.useState(0)

    const cos = React.useMemo(() => {
      return new COS({
        SecretId: "AKIDkMpongR0NbcdaMwJTggVUKzSjonZ7SaU",
        SecretKey: "lIckflfOxJSffR1NYYM3c8tdEdpsnW5l",
      })
    }, [])

    async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
      const file = e.target.files?.[0]
      if (!file) return

      setUploading(true)
      setProgress(0)

      const bucket = "test-1313295794"
      const region = "ap-beijing"
      const key = `${Date.now()}_${file.name}`

      cos.putObject(
        {
          Bucket: bucket,
          Region: region,
          Key: key,
          Body: file,
          onProgress: (progressData) => {
            if (progressData && progressData.percent) {
              setProgress(Math.floor(progressData.percent))
            }
          },
        },
        (err, data) => {
          setUploading(false)
          if (err) {
            alert("上传失败：" + err.message)
          } else {
            // 拼接文件访问地址，按你COS配置可能需要调整
            const url = `https://${bucket}.cos.${region}.myqcloud.com/${key}`
            onUploadSuccess?.(url)
          }
        }
      )
    }

    return (
      <div>
        <Input
          {...props}
          ref={ref}
          type="file"
          accept="image/*"
          className={className}
          onChange={handleFileChange}
          disabled={uploading}
        />
        {uploading && (
          <div className="mt-2 text-sm text-gray-500">上传中... {progress}%</div>
        )}
      </div>
    )
  }
)

ImageInput.displayName = "ImageInput"

