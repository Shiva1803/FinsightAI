import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File } from 'lucide-react'
import clsx from 'clsx'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  accept?: Record<string, string[]>
  label?: string
  selectedFile?: File | null
}

export default function FileUpload({ 
  onFileSelect, 
  accept = { 'image/*': [], 'application/pdf': [] },
  label = 'Upload Document',
  selectedFile 
}: FileUploadProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0])
    }
  }, [onFileSelect])
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    multiple: false,
  })
  
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        {label}
      </label>
      <div
        {...getRootProps()}
        className={clsx(
          'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
          isDragActive
            ? 'border-amber-500 bg-amber-50 dark:bg-amber-900/20'
            : 'border-gray-300 dark:border-gray-600 hover:border-amber-400 dark:hover:border-amber-500 bg-white dark:bg-gray-800'
        )}
      >
        <input {...getInputProps()} />
        
        {selectedFile ? (
          <div className="flex items-center justify-center space-x-2 text-amber-600 dark:text-amber-400">
            <File className="w-6 h-6" />
            <span className="font-medium">{selectedFile.name}</span>
          </div>
        ) : (
          <>
            <Upload className="w-12 h-12 mx-auto text-gray-400 dark:text-gray-500 mb-3" />
            <p className="text-gray-600 dark:text-gray-300 mb-1">
              {isDragActive ? 'Drop the file here' : 'Drag & drop a file here'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">or click to browse</p>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">PDF, PNG, JPG supported</p>
          </>
        )}
      </div>
    </div>
  )
}
