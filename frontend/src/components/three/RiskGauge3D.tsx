import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Text, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

interface RiskGauge3DProps {
  score: number // 0-10
  className?: string
}

function RiskSphere({ score }: { score: number }) {
  const sphereRef = useRef<THREE.Mesh>(null!)
  const glowRef = useRef<THREE.Mesh>(null!)

  // Color based on risk score
  const getColor = (score: number) => {
    if (score >= 7) return '#ef4444' // Red
    if (score >= 4) return '#f59e0b' // Yellow
    return '#10b981' // Green
  }

  const color = getColor(score)
  const fillPercentage = score / 10

  useFrame((state) => {
    const time = state.clock.getElapsedTime()
    if (sphereRef.current) {
      sphereRef.current.rotation.y = time * 0.5
    }
    if (glowRef.current) {
      glowRef.current.scale.setScalar(1 + Math.sin(time * 2) * 0.05)
    }
  })

  return (
    <group>
      {/* Outer glow */}
      <mesh ref={glowRef}>
        <sphereGeometry args={[1.2, 32, 32]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.1}
        />
      </mesh>

      {/* Main sphere */}
      <mesh ref={sphereRef}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.5}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      {/* Fill indicator */}
      <mesh position={[0, -1 + fillPercentage * 2, 0]}>
        <cylinderGeometry args={[1.05, 1.05, 2 - fillPercentage * 2, 32]} />
        <meshBasicMaterial
          color="#000000"
          transparent
          opacity={0.7}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Score text */}
      <Text
        position={[0, 0, 1.1]}
        fontSize={0.5}
        color="white"
        anchorX="center"
        anchorY="middle"
        font="/fonts/inter-bold.woff"
      >
        {score.toFixed(1)}
      </Text>

      {/* Ring indicators */}
      {[0.3, 0.6, 0.9].map((scale, i) => (
        <mesh key={i} rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[1 * scale, 0.01, 16, 100]} />
          <meshBasicMaterial color={color} transparent opacity={0.3} />
        </mesh>
      ))}
    </group>
  )
}

export default function RiskGauge3D({ score, className = '' }: RiskGauge3DProps) {
  return (
    <div className={`w-full h-64 ${className}`}>
      <Canvas camera={{ position: [0, 0, 4], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        <RiskSphere score={score} />
        
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.5}
        />
      </Canvas>
    </div>
  )
}
