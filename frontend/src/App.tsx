import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import Layout from './components/Layout'
import Preloader from './components/Preloader'
import SplashScreen from './components/SplashScreen'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import VerifyDocuments from './pages/VerifyDocuments.tsx'
import UploadDocument from './pages/UploadDocument.tsx'
import Records from './pages/Records.tsx'
import EmailWatcher from './pages/EmailWatcher.tsx'

function App() {
  const [showSplash, setShowSplash] = useState(true)
  const [showPreloader, setShowPreloader] = useState(false)
  const [showContent, setShowContent] = useState(false)

  const handleStart = () => {
    setShowSplash(false)
    setShowPreloader(true)
  }

  const handlePreloaderComplete = () => {
    setShowPreloader(false)
    setShowContent(true)
  }

  return (
    <>
      {showSplash && <SplashScreen onStart={handleStart} />}
      {showPreloader && <Preloader onComplete={handlePreloaderComplete} />}
      {showContent && (
        <div className="animate-fade-in-scale">
          <Router>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
              <Route path="/verify" element={<Layout><VerifyDocuments /></Layout>} />
              <Route path="/upload" element={<Layout><UploadDocument /></Layout>} />
              <Route path="/records" element={<Layout><Records /></Layout>} />
              <Route path="/email-watcher" element={<Layout><EmailWatcher /></Layout>} />
            </Routes>
          </Router>
        </div>
      )}
    </>
  )
}

export default App
