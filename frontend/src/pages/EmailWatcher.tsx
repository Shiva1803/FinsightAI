import { useState, useEffect } from 'react'

interface WatcherStatus {
  running: boolean
  config: {
    imap_host?: string
    imap_user?: string
    check_interval?: number
  }
  stats: {
    status: string
    emails_processed: number
    last_check: string | null
    last_error: string | null
  }
}

export default function EmailWatcher() {
  const [status, setStatus] = useState<WatcherStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    imap_host: '',
    imap_user: '',
    imap_pass: '',
    check_interval: 60
  })

  const fetchStatus = async () => {
    try {
      const res = await fetch('http://localhost:8000/email/watch/status/')
      const data = await res.json()
      setStatus(data)
    } catch (err) {
      console.error('Failed to fetch status:', err)
    }
  }

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const formBody = new URLSearchParams()
      formBody.append('imap_host', formData.imap_host)
      formBody.append('imap_user', formData.imap_user)
      formBody.append('imap_pass', formData.imap_pass)
      formBody.append('check_interval', formData.check_interval.toString())

      const res = await fetch('http://localhost:8000/email/watch/start/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formBody
      })

      if (res.ok) {
        await fetchStatus()
        alert('Email watcher started successfully!')
      } else {
        const error = await res.json()
        alert(`Failed to start: ${error.detail}`)
      }
    } catch (err) {
      alert('Error starting watcher')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleStop = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/email/watch/stop/', {
        method: 'POST'
      })

      if (res.ok) {
        await fetchStatus()
        alert('Email watcher stopped')
      } else {
        const error = await res.json()
        alert(`Failed to stop: ${error.detail}`)
      }
    } catch (err) {
      alert('Error stopping watcher')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Email Watcher</h2>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Automatically monitor your inbox for invoices and purchase orders</p>
      </div>

      {/* Status Card */}
      <div className="card">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Status</h3>
        
        {status && (
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full ${
                status.running ? 'bg-green-500 animate-pulse' : 'bg-gray-400 dark:bg-gray-600'
              }`} />
              <span className="text-gray-900 dark:text-gray-100 font-medium">
                {status.running ? 'Running' : 'Stopped'}
              </span>
            </div>

            {status.running && status.config.imap_host && (
              <div className="text-gray-600 dark:text-gray-400 space-y-1 text-sm">
                <p><strong>Host:</strong> {status.config.imap_host}</p>
                <p><strong>User:</strong> {status.config.imap_user}</p>
                <p><strong>Check Interval:</strong> {status.config.check_interval}s</p>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4">
                <p className="text-amber-600 dark:text-amber-400 text-sm">Emails Processed</p>
                <p className="text-2xl font-bold text-amber-900 dark:text-amber-300">{status.stats.emails_processed}</p>
              </div>
              <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                <p className="text-gray-600 dark:text-gray-400 text-sm">Last Check</p>
                <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {status.stats.last_check || 'Never'}
                </p>
              </div>
            </div>

            {status.stats.last_error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3 mt-4">
                <p className="text-red-700 dark:text-red-300 text-sm">
                  <strong>Error:</strong> {status.stats.last_error}
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Configuration Form */}
      {!status?.running && (
        <div className="card">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Configure Email Watcher</h3>
          
          <form onSubmit={handleStart} className="space-y-4">
            <div>
              <label className="block text-gray-700 dark:text-gray-300 mb-2 font-medium">IMAP Host</label>
              <input
                type="text"
                value={formData.imap_host}
                onChange={(e) => setFormData({ ...formData, imap_host: e.target.value })}
                placeholder="imap.gmail.com"
                className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-gray-700 dark:text-gray-300 mb-2 font-medium">Email Address</label>
              <input
                type="email"
                value={formData.imap_user}
                onChange={(e) => setFormData({ ...formData, imap_user: e.target.value })}
                placeholder="your-email@gmail.com"
                className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-gray-700 dark:text-gray-300 mb-2 font-medium">Password / App Password</label>
              <input
                type="password"
                value={formData.imap_pass}
                onChange={(e) => setFormData({ ...formData, imap_pass: e.target.value })}
                placeholder="••••••••"
                className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-gray-700 dark:text-gray-300 mb-2 font-medium">Check Interval (seconds)</label>
              <input
                type="number"
                value={formData.check_interval}
                onChange={(e) => setFormData({ ...formData, check_interval: parseInt(e.target.value) })}
                min="10"
                className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full"
            >
              {loading ? 'Starting...' : 'Start Watching'}
            </button>
          </form>

          <div className="mt-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
            <p className="text-yellow-800 dark:text-yellow-200 text-sm">
              <strong>Note:</strong> For Gmail, use an App Password instead of your regular password.
              Generate one at: <a href="https://myaccount.google.com/apppasswords" target="_blank" rel="noopener noreferrer" className="underline hover:text-yellow-900 dark:hover:text-yellow-100">Google App Passwords</a>
            </p>
          </div>
        </div>
      )}

      {/* Stop Button */}
      {status?.running && (
        <button
          onClick={handleStop}
          disabled={loading}
          className="w-full py-3 bg-red-600 dark:bg-red-700 text-white font-semibold rounded-lg hover:bg-red-700 dark:hover:bg-red-800 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Stopping...' : 'Stop Watcher'}
        </button>
      )}
    </div>
  )
}
