import { useEffect, useState } from 'react'

interface PreloaderProps {
  onComplete?: () => void
}

export default function Preloader({ onComplete }: PreloaderProps) {
  const [progress, setProgress] = useState(0)
  const [isZooming, setIsZooming] = useState(false)

  useEffect(() => {
    // Simulate loading progress - faster now (3 seconds total)
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval)
          return 100
        }
        return prev + 3.33 // Increment to reach 100 in ~3 seconds
      })
    }, 30)

    // Start zoom animation at 2.7 seconds (before completion)
    const zoomTimer = setTimeout(() => {
      setIsZooming(true)
    }, 2700)

    // Complete and call onComplete after zoom animation
    const completeTimer = setTimeout(() => {
      if (onComplete) onComplete()
    }, 3500) // 2.7s + 0.8s zoom animation

    return () => {
      clearTimeout(zoomTimer)
      clearTimeout(completeTimer)
      clearInterval(progressInterval)
    }
  }, [onComplete])

  return (
    <div className={`fixed inset-0 z-50 flex items-center justify-center bg-gray-900 transition-all duration-700 ${isZooming ? 'opacity-0 scale-150' : 'opacity-100 scale-100'}`}>
      {/* Radial glow effect during zoom */}
      {isZooming && (
        <div className="absolute inset-0 bg-gradient-radial from-amber-500/30 via-transparent to-transparent animate-pulse"></div>
      )}
      
      <div className={`text-center transition-all duration-700 ease-in ${isZooming ? 'scale-[20] opacity-0' : 'scale-100 opacity-100'}`}>
        {/* Logo Animation */}
        <div className="mb-8">
          <div className={`w-32 h-32 mx-auto mb-4 relative transition-all duration-700 ${isZooming ? 'scale-150' : 'scale-100'}`}>
            {/* Chart bars animation - 3 seconds */}
            <div className="absolute inset-0 flex items-end justify-center space-x-2">
              <div 
                className="w-6 bg-gradient-to-t from-amber-500 to-amber-300 rounded-t transition-all duration-500 ease-out"
                style={{ height: `${Math.min(progress * 0.4, 40)}%` }}
              ></div>
              <div 
                className="w-6 bg-gradient-to-t from-amber-500 to-amber-300 rounded-t transition-all duration-500 ease-out"
                style={{ height: `${Math.min(progress * 0.6, 60)}%`, transitionDelay: '50ms' }}
              ></div>
              <div 
                className="w-6 bg-gradient-to-t from-amber-500 to-amber-300 rounded-t transition-all duration-500 ease-out"
                style={{ height: `${Math.min(progress * 0.8, 80)}%`, transitionDelay: '100ms' }}
              ></div>
            </div>
            {/* Arrow - slower bounce */}
            <div className="absolute top-0 right-0 w-8 h-8 text-amber-400 animate-slow-bounce">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M7 17L17 7M17 7H7M17 7V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
              </svg>
            </div>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-amber-600 to-amber-800 dark:from-amber-400 dark:to-amber-600 bg-clip-text text-transparent">
            FinsightAI
          </h1>
        </div>

        {/* Loading spinner */}
        <div className={`flex justify-center space-x-2 mb-4 transition-opacity duration-500 ${isZooming ? 'opacity-0' : 'opacity-100'}`}>
          <div className="w-3 h-3 bg-amber-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
          <div className="w-3 h-3 bg-amber-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          <div className="w-3 h-3 bg-amber-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
        </div>

        <p className={`text-amber-300 font-medium mb-2 transition-opacity duration-500 ${isZooming ? 'opacity-0' : 'opacity-100'}`}>
          Loading your financial insights...
        </p>
        
        {/* Progress bar */}
        <div className={`w-64 mx-auto h-1 bg-gray-800 rounded-full overflow-hidden transition-opacity duration-500 ${isZooming ? 'opacity-0' : 'opacity-100'}`}>
          <div 
            className="h-full bg-gradient-to-r from-amber-400 to-amber-500 transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      <style>{`
        @keyframes slow-bounce {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
        }
        .animate-slow-bounce {
          animation: slow-bounce 2s ease-in-out infinite;
        }
      `}</style>
    </div>
  )
}
