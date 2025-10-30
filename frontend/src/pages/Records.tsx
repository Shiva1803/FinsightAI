import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { Download, FileText, AlertCircle, Trash2, CheckCircle, XCircle } from 'lucide-react'
import { getRecords, deleteRecord } from '../services/api'
import type { Record, VerificationResult, ParsedDocument } from '../types'

// Helper function to check if record is a verification result
const isVerificationRecord = (parsed: any): parsed is VerificationResult => {
  return parsed && 'verification_summary' in parsed
}

// Helper function to get document type display name
const getRecordType = (record: Record): string => {
  if (isVerificationRecord(record.parsed)) {
    return 'Verification'
  }
  return (record.parsed as ParsedDocument).document_type || 'Document'
}

export default function Records() {
  const [records, setRecords] = useState<Record[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedRecord, setSelectedRecord] = useState<Record | null>(null)
  const location = useLocation()
  
  useEffect(() => {
    fetchRecords()
  }, [])
  
  // Handle navigation from Dashboard with selected record ID
  useEffect(() => {
    if (location.state?.selectedRecordId && records.length > 0) {
      const record = records.find(r => r.id === location.state.selectedRecordId)
      if (record) {
        setSelectedRecord(record)
        // Clear the state to avoid re-selecting on refresh
        window.history.replaceState({}, document.title)
      }
    }
  }, [location.state, records])
  
  const fetchRecords = async () => {
    try {
      const data = await getRecords()
      setRecords(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch records')
    } finally {
      setLoading(false)
    }
  }
  
  const handleDeleteRecord = async (recordId: number) => {
    if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
      return
    }
    
    try {
      await deleteRecord(recordId)
      // Remove from local state
      setRecords(records.filter(r => r.id !== recordId))
      // Clear selection if deleted record was selected
      if (selectedRecord?.id === recordId) {
        setSelectedRecord(null)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete record')
    }
  }
  
  const handleExport = async () => {
    try {
      if (records.length === 0) {
        setError('No records to export')
        return
      }
      
      // Create CSV content
      const headers = ['ID', 'Type', 'Vendor Name', 'Document Number', 'PO Number', 'Invoice Date', 'Total Amount', 'Currency', 'Status']
      const rows = records.map(record => {
        if (isVerificationRecord(record.parsed)) {
          return [
            record.id,
            'Verification',
            '',
            '',
            '',
            '',
            '',
            '',
            record.parsed.verification_summary.needs_review ? 'Needs Review' : 'Approved'
          ]
        } else {
          const doc = record.parsed as ParsedDocument
          return [
            record.id,
            doc.document_type || 'Document',
            doc.vendor_name || '',
            doc.document_number || '',
            doc.po_number || '',
            doc.invoice_date || '',
            doc.total_amount || '',
            doc.currency || '',
            ''
          ]
        }
      })
      
      // Create CSV string without gaps
      const csvContent = [
        headers.join(','),
        ...rows.map(row => row.map(cell => {
          // Escape commas and quotes in cell content
          const cellStr = String(cell)
          if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n')) {
            return `"${cellStr.replace(/"/g, '""')}"`
          }
          return cellStr
        }).join(','))
      ].join('\n')
      
      // Download CSV
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `finsightai_export_${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err: any) {
      setError('Failed to export CSV')
    }
  }
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }
  
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Records</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">View all processed documents</p>
        </div>
        <button 
          onClick={handleExport}
          className="btn-primary flex items-center space-x-2"
          disabled={records.length === 0}
        >
          <Download className="w-4 h-4" />
          <span>Export All</span>
        </button>
      </div>
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
          <div>
            <h4 className="font-medium text-red-900">Error</h4>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}
      
      {records.length === 0 ? (
        <div className="card text-center py-12">
          <FileText className="w-16 h-16 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">No Records Found</h3>
          <p className="text-gray-600 dark:text-gray-400">Upload documents to see them here</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">All Records ({records.length})</h3>
            </div>
            <div className="space-y-3 max-h-[600px] overflow-y-auto">
              {records.map((record) => (
                <div
                  key={record.id}
                  onClick={() => setSelectedRecord(record)}
                  className={`card transition-all hover:shadow-md cursor-pointer group ${
                    selectedRecord?.id === record.id ? 'ring-2 ring-amber-500' : ''
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-start space-x-3 flex-1 min-w-0">
                      <div className="bg-amber-100 dark:bg-amber-900/30 p-2 rounded flex-shrink-0">
                        <FileText className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p 
                          className="font-medium text-gray-900 dark:text-gray-100 truncate"
                          title={record.source_file || `Record #${record.id}`}
                        >
                          {record.source_file ? record.source_file.split('/').pop() || record.source_file : `Record #${record.id}`}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1 truncate">
                          {isVerificationRecord(record.parsed) 
                            ? `${record.parsed.po_file} vs ${record.parsed.invoice_file}`
                            : (record.parsed as ParsedDocument).vendor_name || 'Unknown Vendor'}
                        </p>
                        <div className="flex items-center space-x-2 mt-2 flex-wrap gap-1">
                          <span className={`text-xs px-2 py-1 rounded whitespace-nowrap ${
                            isVerificationRecord(record.parsed)
                              ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400'
                              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                          }`}>
                            {getRecordType(record)}
                          </span>
                          {isVerificationRecord(record.parsed) ? (
                            <span className={`text-xs px-2 py-1 rounded whitespace-nowrap ${
                              record.parsed.verification_summary.needs_review
                                ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400'
                                : 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                            }`}>
                              {record.parsed.verification_summary.needs_review ? 'Needs Review' : 'Approved'}
                            </span>
                          ) : (
                            (record.parsed as ParsedDocument).total_amount && (
                              <span className="text-xs bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 px-2 py-1 rounded whitespace-nowrap">
                                ₹{(record.parsed as ParsedDocument).total_amount!.toFixed(2)}
                              </span>
                            )
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 flex-shrink-0">
                      <span className="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">ID: {record.id}</span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleDeleteRecord(record.id)
                        }}
                        className="opacity-0 group-hover:opacity-100 p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-all"
                        title="Delete record"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            {selectedRecord ? (
              <div className="card sticky top-24 max-h-[calc(100vh-120px)] overflow-y-auto">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Record Details</h3>
                
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Basic Information</h4>
                    <dl className="space-y-2">
                      <div className="flex justify-between gap-4">
                        <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Record ID</dt>
                        <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right">{selectedRecord.id}</dd>
                      </div>
                      <div className="flex flex-col gap-1">
                        <dt className="text-sm text-gray-600 dark:text-gray-400">Source File</dt>
                        <dd 
                          className="text-sm font-medium text-gray-900 dark:text-gray-100 break-all"
                          title={selectedRecord.source_file}
                        >
                          {selectedRecord.source_file}
                        </dd>
                      </div>
                      <div className="flex justify-between gap-4">
                        <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Record Type</dt>
                        <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right">{getRecordType(selectedRecord)}</dd>
                      </div>
                    </dl>
                  </div>
                  
                  {isVerificationRecord(selectedRecord.parsed) ? (
                    // Verification Record Details
                    <>
                      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                        <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Verification Summary</h4>
                        <dl className="space-y-2">
                          <div className="flex justify-between gap-4">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">PO File</dt>
                            <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right break-words">{selectedRecord.parsed.po_file}</dd>
                          </div>
                          <div className="flex justify-between gap-4">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Invoice File</dt>
                            <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right break-words">{selectedRecord.parsed.invoice_file}</dd>
                          </div>
                          <div className="flex justify-between gap-4">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Risk Score</dt>
                            <dd className={`text-sm font-bold text-right ${
                              selectedRecord.parsed.anomaly_insights.risk_score >= 7 ? 'text-red-600 dark:text-red-400' :
                              selectedRecord.parsed.anomaly_insights.risk_score >= 4 ? 'text-yellow-600 dark:text-yellow-400' :
                              'text-green-600 dark:text-green-400'
                            }`}>
                              {selectedRecord.parsed.anomaly_insights.risk_score.toFixed(1)}/10
                            </dd>
                          </div>
                          <div className="flex justify-between gap-4">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Status</dt>
                            <dd className={`text-sm font-medium text-right ${
                              selectedRecord.parsed.verification_summary.needs_review
                                ? 'text-yellow-600 dark:text-yellow-400'
                                : 'text-green-600 dark:text-green-400'
                            }`}>
                              {selectedRecord.parsed.verification_summary.needs_review ? 'Needs Review' : 'Approved'}
                            </dd>
                          </div>
                          <div className="flex justify-between gap-4">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Discrepancy Level</dt>
                            <dd className={`text-sm font-medium text-right uppercase ${
                              selectedRecord.parsed.verification_summary.discrepancy_level === 'high' ? 'text-red-600 dark:text-red-400' :
                              selectedRecord.parsed.verification_summary.discrepancy_level === 'medium' ? 'text-yellow-600 dark:text-yellow-400' :
                              selectedRecord.parsed.verification_summary.discrepancy_level === 'low' ? 'text-blue-600 dark:text-blue-400' :
                              'text-green-600 dark:text-green-400'
                            }`}>
                              {selectedRecord.parsed.verification_summary.discrepancy_level}
                            </dd>
                          </div>
                        </dl>
                      </div>
                      
                      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                        <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Match Results</h4>
                        <dl className="space-y-2">
                          <div className="flex justify-between gap-4 items-center">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Vendor Match</dt>
                            <dd className="flex items-center gap-1">
                              {selectedRecord.parsed.verification_summary.vendor_match ? (
                                <><CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" /><span className="text-sm text-green-600 dark:text-green-400">Matched</span></>
                              ) : (
                                <><XCircle className="w-4 h-4 text-red-600 dark:text-red-400" /><span className="text-sm text-red-600 dark:text-red-400">Mismatch</span></>
                              )}
                            </dd>
                          </div>
                          <div className="flex justify-between gap-4 items-center">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Amount Match</dt>
                            <dd className="flex items-center gap-1">
                              {selectedRecord.parsed.verification_summary.total_match ? (
                                <><CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" /><span className="text-sm text-green-600 dark:text-green-400">Matched</span></>
                              ) : (
                                <><XCircle className="w-4 h-4 text-red-600 dark:text-red-400" /><span className="text-sm text-red-600 dark:text-red-400">Diff: ₹{selectedRecord.parsed.verification_summary.amount_difference}</span></>
                              )}
                            </dd>
                          </div>
                          <div className="flex justify-between gap-4 items-center">
                            <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Quantity Match</dt>
                            <dd className="flex items-center gap-1">
                              {(() => {
                                // Calculate quantity match from line items
                                const lineItems = selectedRecord.parsed.visualization_data.line_items_comparison
                                const quantityMatch = lineItems.length === 0 || lineItems.every(item => item.qty_match)
                                const mismatchCount = lineItems.filter(item => !item.qty_match).length
                                
                                return quantityMatch ? (
                                  <><CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" /><span className="text-sm text-green-600 dark:text-green-400">Matched</span></>
                                ) : (
                                  <><XCircle className="w-4 h-4 text-red-600 dark:text-red-400" /><span className="text-sm text-red-600 dark:text-red-400">{mismatchCount} Mismatch{mismatchCount !== 1 ? 'es' : ''}</span></>
                                )
                              })()}
                            </dd>
                          </div>
                        </dl>
                      </div>
                      
                      {selectedRecord.parsed.anomaly_insights.anomaly_detected && (
                        <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2 flex items-center">
                            <AlertCircle className="w-4 h-4 text-yellow-600 dark:text-yellow-400 mr-2" />
                            Anomalies Detected
                          </h4>
                          <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">{selectedRecord.parsed.anomaly_insights.anomaly_reason}</p>
                          {selectedRecord.parsed.anomaly_insights.fraud_indicators.length > 0 && (
                            <div className="mt-2">
                              <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Fraud Indicators:</p>
                              <ul className="list-disc list-inside space-y-1">
                                {selectedRecord.parsed.anomaly_insights.fraud_indicators.map((indicator, idx) => (
                                  <li key={idx} className="text-xs text-yellow-700 dark:text-yellow-400">{indicator}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                      
                      {selectedRecord.parsed.visualization_data.discrepancy_count > 0 && (
                        <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                          <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Discrepancy Breakdown</h4>
                          <div className="space-y-2">
                            {Object.entries(selectedRecord.parsed.visualization_data.pie_chart.discrepancy_breakdown)
                              .filter(([_, value]) => (value as number) > 0)
                              .map(([name, value]) => (
                                <div key={name} className="flex justify-between gap-4 text-sm">
                                  <span className="text-gray-600 dark:text-gray-400">{name}</span>
                                  <span className="font-medium text-gray-900 dark:text-gray-100">{value as number}</span>
                                </div>
                              ))}
                          </div>
                        </div>
                      )}
                    </>
                  ) : (
                    // Document Record Details
                    <>
                  
                    <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Document Details</h4>
                      <dl className="space-y-2">
                        <div className="flex justify-between gap-4">
                          <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Vendor</dt>
                          <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right break-words">{(selectedRecord.parsed as ParsedDocument).vendor_name || 'N/A'}</dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Document #</dt>
                          <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right break-words">{(selectedRecord.parsed as ParsedDocument).document_number || 'N/A'}</dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">PO Number</dt>
                          <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right break-words">{(selectedRecord.parsed as ParsedDocument).po_number || 'N/A'}</dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Date</dt>
                          <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right">{(selectedRecord.parsed as ParsedDocument).invoice_date || 'N/A'}</dd>
                        </div>
                      </dl>
                    </div>
                  
                    <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Financial</h4>
                      <dl className="space-y-2">
                        <div className="flex justify-between gap-4">
                          <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Currency</dt>
                          <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right">{(selectedRecord.parsed as ParsedDocument).currency || 'N/A'}</dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Subtotal</dt>
                          <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right">
                            {(selectedRecord.parsed as ParsedDocument).subtotal_amount ? `₹${(selectedRecord.parsed as ParsedDocument).subtotal_amount!.toFixed(2)}` : 'N/A'}
                          </dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">Tax</dt>
                          <dd className="text-sm font-medium text-gray-900 dark:text-gray-100 text-right">
                            {(selectedRecord.parsed as ParsedDocument).tax_amount ? `₹${(selectedRecord.parsed as ParsedDocument).tax_amount!.toFixed(2)}` : 'N/A'}
                          </dd>
                        </div>
                        <div className="flex justify-between gap-4 pt-2 border-t border-gray-200 dark:border-gray-700">
                          <dt className="text-sm font-medium text-gray-900 dark:text-gray-100 flex-shrink-0">Total</dt>
                          <dd className="text-sm font-bold text-amber-600 dark:text-amber-400 text-right">
                            {(selectedRecord.parsed as ParsedDocument).total_amount ? `₹${(selectedRecord.parsed as ParsedDocument).total_amount!.toFixed(2)}` : 'N/A'}
                          </dd>
                        </div>
                      </dl>
                    </div>
                    
                    {(selectedRecord.parsed as ParsedDocument).line_items && (selectedRecord.parsed as ParsedDocument).line_items.length > 0 && (
                      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                        <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Line Items ({(selectedRecord.parsed as ParsedDocument).line_items.length})</h4>
                        <div className="space-y-2 max-h-40 overflow-y-auto">
                          {(selectedRecord.parsed as ParsedDocument).line_items.map((item, idx) => (
                            <div key={idx} className="text-sm bg-gray-50 dark:bg-gray-700/50 p-2 rounded">
                              <p className="font-medium text-gray-900 dark:text-gray-100 break-words">{item.description}</p>
                              <p className="text-gray-600 dark:text-gray-400">
                                Qty: {item.quantity ?? 'N/A'} × ₹{item.unit_price?.toFixed(2) ?? 'N/A'}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {(selectedRecord.parsed as ParsedDocument).extraction_warnings && (selectedRecord.parsed as ParsedDocument).extraction_warnings.length > 0 && (
                      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                        <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2 flex items-center">
                          <AlertCircle className="w-4 h-4 text-yellow-600 dark:text-yellow-500 mr-2" />
                          Warnings
                        </h4>
                        <ul className="list-disc list-inside space-y-1">
                          {(selectedRecord.parsed as ParsedDocument).extraction_warnings.map((warning, idx) => (
                            <li key={idx} className="text-xs text-yellow-700 dark:text-yellow-400 break-words">{warning}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}
                </div>
              </div>
            ) : (
              <div className="card text-center py-12">
                <FileText className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-3" />
                <p className="text-gray-600 dark:text-gray-400">Select a record to view details</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
