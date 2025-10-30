import { useState } from 'react'
import { AlertCircle, CheckCircle, XCircle, TrendingUp } from 'lucide-react'
import FileUpload from '../components/FileUpload'
import { verifyDocuments } from '../services/api'
import type { VerificationResult } from '../types'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function VerifyDocuments() {
  const [poFile, setPoFile] = useState<File | null>(null)
  const [invoiceFile, setInvoiceFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<VerificationResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  
  const handleVerify = async () => {
    if (!poFile || !invoiceFile) {
      setError('Please upload both PO and Invoice files')
      return
    }
    
    setLoading(true)
    setError(null)
    
    try {
      const data = await verifyDocuments(poFile, invoiceFile)
      setResult(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to verify documents')
    } finally {
      setLoading(false)
    }
  }
  
  const getRiskColor = (score: number) => {
    if (score >= 7) return 'text-red-600'
    if (score >= 4) return 'text-yellow-600'
    return 'text-green-600'
  }
  
  const getDiscrepancyColor = (level: string) => {
    switch (level) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-blue-100 text-blue-800'
      default: return 'bg-green-100 text-green-800'
    }
  }
  
  const COLORS = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6', '#ec4899']
  
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Verify Documents</h2>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Compare Purchase Order and Invoice for discrepancies</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <FileUpload
          label="Purchase Order (PO)"
          onFileSelect={setPoFile}
          selectedFile={poFile}
        />
        <FileUpload
          label="Invoice"
          onFileSelect={setInvoiceFile}
          selectedFile={invoiceFile}
        />
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
      
      <button
        onClick={handleVerify}
        disabled={loading || !poFile || !invoiceFile}
        className="btn-primary w-full md:w-auto"
      >
        {loading ? 'Verifying...' : 'Verify Documents'}
      </button>
      
      {result && (
        <div className="space-y-6">
          <div className="card bg-gradient-to-r from-amber-50 to-amber-100 dark:from-amber-900/20 dark:to-amber-800/20">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Verification Summary</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {result.po_file} vs {result.invoice_file}
                </p>
              </div>
              <div className="text-right">
                <div className={`text-3xl font-bold ${getRiskColor(result.anomaly_insights.risk_score)}`}>
                  {result.anomaly_insights.risk_score.toFixed(1)}/10
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Risk Score</p>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="card">
              <div className="flex items-center space-x-3">
                {result.verification_summary.vendor_match ? (
                  <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
                ) : (
                  <XCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
                )}
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Vendor Match</p>
                  <p className="font-semibold text-gray-900 dark:text-gray-100">{result.verification_summary.vendor_match ? 'Matched' : 'Mismatch'}</p>
                </div>
              </div>
            </div>
            
            <div className="card">
              <div className="flex items-center space-x-3">
                {result.verification_summary.total_match ? (
                  <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
                ) : (
                  <XCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
                )}
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Amount Match</p>
                  <p className="font-semibold text-gray-900 dark:text-gray-100">
                    {result.verification_summary.total_match ? 'Matched' : `Diff: ₹${result.verification_summary.amount_difference}`}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="card">
              <div className="flex items-center space-x-3">
                {(() => {
                  // Calculate quantity match from line items
                  const lineItems = result.visualization_data.line_items_comparison
                  const quantityMatch = lineItems.length === 0 || lineItems.every(item => item.qty_match)
                  const mismatchCount = lineItems.filter(item => !item.qty_match).length
                  
                  return (
                    <>
                      {quantityMatch ? (
                        <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
                      ) : (
                        <XCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
                      )}
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Quantity Match</p>
                        <p className="font-semibold text-gray-900 dark:text-gray-100">
                          {quantityMatch ? 'Matched' : `${mismatchCount} Mismatch${mismatchCount !== 1 ? 'es' : ''}`}
                        </p>
                      </div>
                    </>
                  )
                })()}
              </div>
            </div>
            
            <div className="card">
              <div className="flex items-center space-x-3">
                <TrendingUp className={`w-6 h-6 ${result.verification_summary.needs_review ? 'text-yellow-600 dark:text-yellow-400' : 'text-green-600 dark:text-green-400'}`} />
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Status</p>
                  <p className="font-semibold text-gray-900 dark:text-gray-100">{result.verification_summary.needs_review ? 'Needs Review' : 'Approved'}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Discrepancy Level</h4>
            <span className={`inline-block px-4 py-2 rounded-full font-medium ${getDiscrepancyColor(result.verification_summary.discrepancy_level)}`}>
              {result.verification_summary.discrepancy_level.toUpperCase()}
            </span>
          </div>
          
          {result.anomaly_insights.anomaly_detected && (
            <div className="card bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3 flex items-center">
                <AlertCircle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-2" />
                Anomalies Detected
              </h4>
              <p className="text-gray-700 dark:text-gray-300 mb-4">{result.anomaly_insights.anomaly_reason}</p>
              
              {result.anomaly_insights.fraud_indicators.length > 0 && (
                <div>
                  <p className="font-medium text-gray-900 dark:text-gray-100 mb-2">Fraud Indicators:</p>
                  <ul className="list-disc list-inside space-y-1">
                    {result.anomaly_insights.fraud_indicators.map((indicator, idx) => (
                      <li key={idx} className="text-sm text-gray-700 dark:text-gray-300">{indicator}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Amount Comparison</h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={[
                  { name: result.visualization_data.bar_chart.labels[0], amount: result.visualization_data.bar_chart.values[0] },
                  { name: result.visualization_data.bar_chart.labels[1], amount: result.visualization_data.bar_chart.values[1] }
                ]}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="amount" fill="#0ea5e9" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            <div className="card">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Discrepancy Breakdown</h4>
              {Object.values(result.visualization_data.pie_chart.discrepancy_breakdown).some((v) => (v as number) > 0) ? (
                <>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={Object.entries(result.visualization_data.pie_chart.discrepancy_breakdown)
                          .filter(([_, value]) => (value as number) > 0)
                          .map(([name, value]) => ({ 
                            name: name === 'Price' ? 'Price Mismatch' : 
                                  name === 'Quantity' ? 'Quantity Mismatch' :
                                  name === 'Amount' ? 'Amount Mismatch' :
                                  name === 'Tax' ? 'Tax Mismatch' :
                                  name === 'Vendor Name' ? 'Vendor Mismatch' :
                                  name,
                            value,
                            originalName: name
                          }))}
                        cx="50%"
                        cy="50%"
                        labelLine={true}
                        label={({ percent }: any) => `${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {Object.entries(result.visualization_data.pie_chart.discrepancy_breakdown)
                          .filter(([_, value]) => (value as number) > 0)
                          .map((_, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                      </Pie>
                      <Tooltip 
                        formatter={(value: any, _name: string, props: any) => [
                          `${value} issue${value !== 1 ? 's' : ''}`,
                          props.payload.name
                        ]}
                      />
                      <Legend 
                        verticalAlign="bottom" 
                        height={36}
                        formatter={(value, entry: any) => {
                          const count = entry.payload.value
                          return `${value} (${count})`
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                  
                  {/* Detailed Breakdown List */}
                  <div className="mt-6 space-y-2">
                    <h5 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Detailed Breakdown:</h5>
                    {Object.entries(result.visualization_data.pie_chart.discrepancy_breakdown)
                      .filter(([_, value]) => (value as number) > 0)
                      .map(([name, value], index) => {
                        const numValue = value as number
                        const total = Object.values(result.visualization_data.pie_chart.discrepancy_breakdown).reduce((a, b) => (a as number) + (b as number), 0) as number
                        const percentage = (numValue / total * 100).toFixed(1)
                        const displayName = name === 'Price' ? 'Price Mismatch' : 
                                          name === 'Quantity' ? 'Quantity Mismatch' :
                                          name === 'Amount' ? 'Amount Mismatch' :
                                          name === 'Tax' ? 'Tax Mismatch' :
                                          name === 'Vendor Name' ? 'Vendor Mismatch' :
                                          name
                        return (
                          <div key={name} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                            <div className="flex items-center space-x-3">
                              <div 
                                className="w-4 h-4 rounded-full" 
                                style={{ backgroundColor: COLORS[index % COLORS.length] }}
                              />
                              <span className="font-medium text-gray-900 dark:text-gray-100">{displayName}</span>
                            </div>
                            <div className="text-right">
                              <span className="text-lg font-bold text-gray-900 dark:text-gray-100">{percentage}%</span>
                              <span className="text-sm text-gray-500 dark:text-gray-400 ml-2">({numValue} issue{numValue !== 1 ? 's' : ''})</span>
                            </div>
                          </div>
                        )
                      })}
                  </div>
                </>
              ) : (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  <CheckCircle className="w-12 h-12 mx-auto mb-2 text-green-500" />
                  <p>No discrepancies found!</p>
                </div>
              )}
            </div>
          </div>
          
          {result.visualization_data.line_items_comparison.length > 0 && (
            <div className="card">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Line Items Comparison</h4>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Description</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">PO Qty</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Invoice Qty</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">PO Price</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Invoice Price</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Status</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    {result.visualization_data.line_items_comparison.map((item, idx) => (
                      <tr key={idx}>
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">{item.description}</td>
                        <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{item.po_qty ?? '-'}</td>
                        <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{item.invoice_qty ?? '-'}</td>
                        <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{item.po_price ?? '-'}</td>
                        <td className="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{item.invoice_price ?? '-'}</td>
                        <td className="px-4 py-3 text-sm">
                          {item.qty_match && item.price_match ? (
                            <span className="text-green-600 dark:text-green-400 font-medium">✓ Match</span>
                          ) : (
                            <span className="text-red-600 dark:text-red-400 font-medium">✗ Mismatch</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
