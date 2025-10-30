import { ReactNode, useRef, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { RoundedBox } from '@react-three/drei'
import * as THREE from 'three'

interface Card3DProps {
  children: ReactNode
  className?: string
  glowColor?: string
}

function FloatingCard({ isHovered }: { isHovered: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null!)

  useFrame((state) => {
    if (meshRef.current) {
      const time = state.clock.getElapsedTime()
      meshRef.current.position.y = Math.sin(time * 0.5) * 0.1
      meshRef.current.rotation.x = isHovered ? -0.1 : Math.sin(time * 0.3) * 0.05
      meshRef.current.rotation.y = isHovered ? 0.1 : Math.cos(time * 0.3) * 0.05
    }
  })

  return (
    <RoundedBox
      ref={meshRef}
      args={[4, 3, 0.2]}
      radius={0.1}
      smoothness={4}
    >
      <meshStandardMaterial
        color="#1e293b"
        transparent
        opacity={0.3}
        metalness={0.8}
        roughness={0.2}
      />
    </RoundedBox>
  )
}

export default function Card3D({ children, className = '', glowColor = '#0ea5e9' }: Card3DProps) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div
      className={`relative ${className}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* 3D Background */}
      <div className="absolute inset-0 -z-10">
        <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[5, 5, 5]} intensity={0.5} color={glowColor} />
          <FloatingCard isHovered={isHovered} />
        </Canvas>
      </div>

      {/* Content */}
      <div
        className={`relative bg-gray-900/50 backdrop-blur-md rounded-xl p-6 border border-gray-700/50 transition-all duration-300 ${
          isHovered ? 'transform scale-105 shadow-2xl' : ''
        }`}
        style={{
          boxShadow: isHovered ? `0 20px 60px ${glowColor}40` : 'none'
        }}
      >
        {children}
      </div>
    </div>
  )
}
