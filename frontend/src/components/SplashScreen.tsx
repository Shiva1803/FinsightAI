import { ArrowRight } from 'lucide-react'
import { useDistortionEffect } from '../hooks/useDistortionEffect'

interface SplashScreenProps {
  onStart: () => void
}

export default function SplashScreen({ onStart }: SplashScreenProps) {
  const { canvasRef, imageRef } = useDistortionEffect(true)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 overflow-hidden">
      {/* Animated background particles */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-amber-500 rounded-full filter blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-amber-600 rounded-full filter blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="relative text-center space-y-12 animate-fade-in">
        {/* Logo and Name */}
        <div className="space-y-6">
          {/* Logo Image with WebGL Distortion */}
          <div className="flex items-center justify-center mb-8 relative">
            <div className="relative w-64 h-64 group cursor-pointer">
              {/* Hidden image for WebGL texture */}
              <img 
                ref={imageRef}
                src="/logo.png" 
                alt="FinsightAI Logo" 
                className="absolute inset-0 w-full h-full object-contain opacity-0 pointer-events-none"
                crossOrigin="anonymous"
                onError={() => {
                  // If logo fails to load, hide canvas and show fallback
                  const canvas = canvasRef.current
                  if (canvas) canvas.style.display = 'none'
                  const fallback = document.getElementById('logo-fallback')
                  if (fallback) fallback.style.display = 'block'
                }}
              />
              
              {/* WebGL Canvas for distortion effect */}
              <canvas
                ref={canvasRef}
                width={512}
                height={512}
                className="w-full h-full object-contain transition-all duration-300 group-hover:scale-105"
              />
              
              {/* Fallback SVG (hidden by default) */}
              <div id="logo-fallback" className="absolute inset-0 hidden">
                <div className="w-full h-full flex items-center justify-center">
                  <div className="w-40 h-40 relative">
                    {/* Chart bars */}
                    <div className="absolute inset-0 flex items-end justify-center space-x-3">
                      <div className="w-8 h-16 bg-gradient-to-t from-amber-500 to-amber-300 rounded-t transform transition-transform group-hover:scale-110"></div>
                      <div className="w-8 h-24 bg-gradient-to-t from-amber-500 to-amber-300 rounded-t transform transition-transform group-hover:scale-110" style={{ transitionDelay: '50ms' }}></div>
                      <div className="w-8 h-32 bg-gradient-to-t from-amber-500 to-amber-300 rounded-t transform transition-transform group-hover:scale-110" style={{ transitionDelay: '100ms' }}></div>
                    </div>
                    {/* Arrow */}
                    <div className="absolute -top-2 -right-2 w-10 h-10 text-amber-400 animate-bounce">
                      <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M7 17L17 7M17 7H7M17 7V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>

              {/* Glow effect on hover */}
              <div className="absolute inset-0 bg-gradient-to-r from-amber-500/0 via-amber-400/20 to-amber-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl pointer-events-none"></div>
            </div>
          </div>
          
          <h1 className="text-6xl font-bold bg-gradient-to-r from-amber-400 to-amber-600 bg-clip-text text-transparent animate-pulse">
            FinsightAI
          </h1>
          <p className="text-xl text-amber-300 font-medium">
            Intelligent Document Processing
          </p>
        </div>

        {/* Start Button */}
        <button
          onClick={onStart}
          className="group relative inline-flex items-center space-x-3 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-white px-10 py-4 rounded-full text-lg font-semibold shadow-lg hover:shadow-2xl hover:shadow-amber-500/50 transition-all duration-300 transform hover:scale-105"
        >
          <span>Get Started</span>
          <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
          
          {/* Button glow effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-amber-400 to-amber-600 rounded-full opacity-0 group-hover:opacity-30 blur-xl transition-opacity duration-300"></div>
        </button>
      </div>
    </div>
  )
}
