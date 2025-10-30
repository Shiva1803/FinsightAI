import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { CheckCircle, Upload, AlertTriangle, TrendingUp } from 'lucide-react'
import { getRecords, healthCheck } from '../services/api'
import type { Record } from '../types'

export default function Dashboard() {
  const [records, setRecords] = useState<Record[]>([])
  const [loading, setLoading] = useState(true)
  const [healthStatus, setHealthStatus] = useState<string>('checking')
  const navigate = useNavigate()
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [recordsData, health] = await Promise.all([
          getRecords(),
          healthCheck()
        ])
        setRecords(recordsData)
        setHealthStatus(health.status)
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
        setHealthStatus('error')
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [])
  
  // Helper to check if record is verification
  const isVerificationRecord = (parsed: any) => {
    return parsed && 'verification_summary' in parsed
  }

  const stats = [
    {
      label: 'Total Documents',
      value: records.length,
      icon: Upload,
      color: 'bg-blue-500',
    },
    {
      label: 'Verified',
      value: records.filter(r => isVerificationRecord(r.parsed)).length,
      icon: CheckCircle,
      color: 'bg-green-500',
    },
    {
      label: 'Needs Review',
      value: records.filter(r => {
        if (isVerificationRecord(r.parsed)) {
          return (r.parsed as any).verification_summary?.needs_review
        }
        return (r.parsed as any).extraction_warnings?.length > 0
      }).length,
      icon: AlertTriangle,
      color: 'bg-yellow-500',
    },
    {
      label: 'System Status',
      value: healthStatus === 'ok' ? 'Healthy' : 'Error',
      icon: TrendingUp,
      color: healthStatus === 'ok' ? 'bg-green-500' : 'bg-red-500',
    },
  ]
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }
  
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Dashboard</h2>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Overview of your document verification system</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-1">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link to="/verify" className="card hover:shadow-md transition-shadow cursor-pointer group">
          <div className="flex items-center space-x-4">
            <div className="bg-amber-100 dark:bg-amber-900/30 p-4 rounded-lg group-hover:bg-amber-200 dark:group-hover:bg-amber-900/50 transition-colors">
              <CheckCircle className="w-8 h-8 text-amber-600 dark:text-amber-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Verify Documents</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Compare PO and Invoice for discrepancies</p>
            </div>
          </div>
        </Link>
        
        <Link to="/upload" className="card hover:shadow-md transition-shadow cursor-pointer group">
          <div className="flex items-center space-x-4">
            <div className="bg-green-100 dark:bg-green-900/30 p-4 rounded-lg group-hover:bg-green-200 dark:group-hover:bg-green-900/50 transition-colors">
              <Upload className="w-8 h-8 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Upload Document</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Extract data from invoices and POs</p>
            </div>
          </div>
        </Link>
      </div>
      
      <div className="card">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Recent Activity</h3>
        {records.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-8">No documents processed yet</p>
        ) : (
          <div className="space-y-3">
            {records.slice(-5).reverse().map((record) => (
              <div 
                key={record.id} 
                onClick={() => navigate('/records', { state: { selectedRecordId: record.id } })}
                className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors cursor-pointer"
              >
                <div className="flex items-center space-x-3 flex-1">
                  <div className="bg-amber-100 dark:bg-amber-900/30 p-2 rounded">
                    <Upload className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 dark:text-gray-100">{record.source_file || 'Unknown'}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {isVerificationRecord(record.parsed) 
                        ? `${(record.parsed as any).po_file} vs ${(record.parsed as any).invoice_file}`
                        : `${(record.parsed as any).vendor_name || 'No vendor'} • ${(record.parsed as any).document_type}`
                      }
                    </p>
                  </div>
                </div>
                <span className="text-sm text-gray-500 dark:text-gray-400">ID: {record.id}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
