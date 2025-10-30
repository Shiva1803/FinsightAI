import { useState } from 'react'
import { AlertCircle, CheckCircle } from 'lucide-react'
import FileUpload from '../components/FileUpload'
import { uploadDocument } from '../services/api'
import type { ParsedDocument } from '../types'

export default function UploadDocument() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{ id: number; parsed: ParsedDocument } | null>(null)
  const [error, setError] = useState<string | null>(null)
  
  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload')
      return
    }
    
    setLoading(true)
    setError(null)
    
    try {
      const data = await uploadDocument(file)
      setResult(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload document')
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Upload Document</h2>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Extract data from invoices and purchase orders</p>
      </div>
      
      <div className="max-w-2xl">
        <FileUpload
          label="Select Document"
          onFileSelect={setFile}
          selectedFile={file}
        />
      </div>
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3 max-w-2xl">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
          <div>
            <h4 className="font-medium text-red-900">Error</h4>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}
      
      <button
        onClick={handleUpload}
        disabled={loading || !file}
        className="btn-primary"
      >
        {loading ? 'Processing...' : 'Upload & Extract'}
      </button>
      
      {result && (
        <div className="space-y-6">
          <div className="card bg-green-50 border-green-200">
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-6 h-6 text-green-600" />
              <div>
                <h4 className="font-medium text-green-900">Document Processed Successfully</h4>
                <p className="text-sm text-green-700">Record ID: {result.id}</p>
              </div>
            </div>
          </div>
          
          <div className="card">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Extracted Data</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Document Information</h4>
                <dl className="space-y-2">
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Type</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.document_type}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Document Number</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.document_number || 'N/A'}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">PO Number</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.po_number || 'N/A'}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Date</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.invoice_date || 'N/A'}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Due Date</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.due_date || 'N/A'}</dd>
                  </div>
                </dl>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Parties</h4>
                <dl className="space-y-2">
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Vendor Name</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.vendor_name || 'N/A'}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Vendor Tax ID</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.vendor_tax_id || 'N/A'}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Buyer Name</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.buyer_name || 'N/A'}</dd>
                  </div>
                  <div>
                    <dt className="text-sm text-gray-600 dark:text-gray-400">Buyer Tax ID</dt>
                    <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.parsed.buyer_tax_id || 'N/A'}</dd>
                  </div>
                </dl>
              </div>
            </div>
            
            <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Financial Details</h4>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400">Currency</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">{result.parsed.currency || 'N/A'}</p>
                </div>
                <div className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400">Subtotal</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    {result.parsed.subtotal_amount ? `₹${result.parsed.subtotal_amount.toFixed(2)}` : 'N/A'}
                  </p>
                </div>
                <div className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400">Tax</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    {result.parsed.tax_amount ? `₹${result.parsed.tax_amount.toFixed(2)}` : 'N/A'}
                  </p>
                </div>
                <div className="bg-amber-50 dark:bg-amber-900/20 p-4 rounded-lg">
                  <p className="text-sm text-amber-600 dark:text-amber-400">Total Amount</p>
                  <p className="text-lg font-semibold text-amber-900 dark:text-amber-300">
                    {result.parsed.total_amount ? `₹${result.parsed.total_amount.toFixed(2)}` : 'N/A'}
                  </p>
                </div>
              </div>
            </div>
            
            {result.parsed.line_items && result.parsed.line_items.length > 0 && (
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Line Items</h4>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead className="bg-gray-50 dark:bg-gray-800">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Description</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">SKU</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Quantity</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Unit Price</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Total</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                      {result.parsed.line_items.map((item, idx) => (
                        <tr key={idx}>
                          <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">{item.description}</td>
                          <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{item.sku || '-'}</td>
                          <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{item.quantity ?? '-'}</td>
                          <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">
                            {item.unit_price ? `₹${item.unit_price.toFixed(2)}` : '-'}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">
                            {item.line_total ? `₹${item.line_total.toFixed(2)}` : '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
            
            {result.parsed.extraction_warnings && result.parsed.extraction_warnings.length > 0 && (
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3 flex items-center">
                  <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-2" />
                  Extraction Warnings
                </h4>
                <ul className="list-disc list-inside space-y-1">
                  {result.parsed.extraction_warnings.map((warning, idx) => (
                    <li key={idx} className="text-sm text-yellow-700 dark:text-yellow-400">{warning}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
