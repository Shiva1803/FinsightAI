import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Text, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

interface BarChart3DProps {
  data: Array<{ label: string; value: number }>
  color?: string
  className?: string
}

function Bar3D({ position, height, color, label, value }: {
  position: [number, number, number]
  height: number
  color: string
  label: string
  value: number
}) {
  const meshRef = useRef<THREE.Mesh>(null!)
  const targetHeight = useRef(height)
  const currentHeight = useRef(0)

  useFrame(() => {
    // Animate height
    if (currentHeight.current < targetHeight.current) {
      currentHeight.current += 0.05
      if (meshRef.current) {
        meshRef.current.scale.y = currentHeight.current / targetHeight.current
      }
    }
  })

  return (
    <group position={position}>
      {/* Bar */}
      <mesh ref={meshRef} position={[0, height / 2, 0]}>
        <boxGeometry args={[0.8, height, 0.8]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.3}
          metalness={0.5}
          roughness={0.3}
        />
      </mesh>

      {/* Base */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[1, 0.1, 1]} />
        <meshStandardMaterial color="#1e293b" />
      </mesh>

      {/* Label */}
      <Text
        position={[0, -0.3, 0]}
        fontSize={0.2}
        color="white"
        anchorX="center"
        anchorY="top"
        rotation={[-Math.PI / 6, 0, 0]}
      >
        {label}
      </Text>

      {/* Value */}
      <Text
        position={[0, height + 0.3, 0]}
        fontSize={0.25}
        color={color}
        anchorX="center"
        anchorY="bottom"
      >
        {value.toLocaleString()}
      </Text>
    </group>
  )
}

export default function BarChart3D({ data, color = '#0ea5e9', className = '' }: BarChart3DProps) {
  const maxValue = Math.max(...data.map(d => d.value))
  const spacing = 2

  return (
    <div className={`w-full h-96 ${className}`}>
      <Canvas camera={{ position: [0, 3, 8], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, 10, -10]} intensity={0.5} />
        <spotLight position={[0, 10, 0]} angle={0.3} penumbra={1} intensity={1} />

        {/* Grid */}
        <gridHelper args={[20, 20, '#334155', '#1e293b']} position={[0, 0, 0]} />

        {/* Bars */}
        {data.map((item, index) => {
          const height = (item.value / maxValue) * 4
          const x = (index - (data.length - 1) / 2) * spacing
          return (
            <Bar3D
              key={item.label}
              position={[x, 0, 0]}
              height={height}
              color={color}
              label={item.label}
              value={item.value}
            />
          )
        })}

        <OrbitControls
          enableZoom={true}
          enablePan={false}
          minPolarAngle={Math.PI / 6}
          maxPolarAngle={Math.PI / 2}
        />
      </Canvas>
    </div>
  )
}

// Pie Chart 3D Component
interface PieChart3DProps {
  data: Array<{ label: string; value: number; color: string }>
  className?: string
}

function PieSlice({ startAngle, endAngle, color, radius, label, value }: {
  startAngle: number
  endAngle: number
  color: string
  radius: number
  label: string
  value: number
}) {
  const meshRef = useRef<THREE.Mesh>(null!)

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 0.5) * 0.02
    }
  })

  const angle = endAngle - startAngle
  const midAngle = startAngle + angle / 2

  return (
    <group>
      <mesh
        ref={meshRef}
        rotation={[0, 0, startAngle]}
        position={[
          Math.cos(midAngle) * 0.1,
          Math.sin(midAngle) * 0.1,
          0
        ]}
      >
        <cylinderGeometry args={[radius, radius, 0.5, 32, 1, false, 0, angle]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.2}
          metalness={0.5}
          roughness={0.3}
        />
      </mesh>

      {/* Label */}
      <Text
        position={[
          Math.cos(midAngle) * (radius + 0.8),
          Math.sin(midAngle) * (radius + 0.8),
          0.3
        ]}
        fontSize={0.2}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {label}
      </Text>

      {/* Value */}
      <Text
        position={[
          Math.cos(midAngle) * (radius + 0.8),
          Math.sin(midAngle) * (radius + 0.8),
          0
        ]}
        fontSize={0.15}
        color={color}
        anchorX="center"
        anchorY="middle"
      >
        {value}
      </Text>
    </group>
  )
}

export function PieChart3D({ data, className = '' }: PieChart3DProps) {
  const total = data.reduce((sum, item) => sum + item.value, 0)
  let currentAngle = 0

  return (
    <div className={`w-full h-96 ${className}`}>
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />

        <group rotation={[Math.PI / 2, 0, 0]}>
          {data.map((item, index) => {
            const angle = (item.value / total) * Math.PI * 2
            const slice = (
              <PieSlice
                key={index}
                startAngle={currentAngle}
                endAngle={currentAngle + angle}
                color={item.color}
                radius={2}
                label={item.label}
                value={item.value}
              />
            )
            currentAngle += angle
            return slice
          })}
        </group>

        <OrbitControls
          enableZoom={true}
          enablePan={false}
          autoRotate
          autoRotateSpeed={2}
        />
      </Canvas>
    </div>
  )
}
