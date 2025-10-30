import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { RoundedBox, Text } from '@react-three/drei'
import * as THREE from 'three'

interface DocumentPreview3DProps {
  fileName: string
  fileType: string
  isUploading?: boolean
  progress?: number
  className?: string
}

function Document3D({ fileName, isUploading, progress = 0 }: {
  fileName: string
  isUploading: boolean
  progress: number
}) {
  const docRef = useRef<THREE.Group>(null!)
  const progressRef = useRef<THREE.Mesh>(null!)

  useFrame((state) => {
    if (docRef.current) {
      if (isUploading) {
        docRef.current.rotation.y = state.clock.getElapsedTime() * 2
      } else {
        docRef.current.rotation.y = Math.sin(state.clock.getElapsedTime() * 0.5) * 0.2
        docRef.current.position.y = Math.sin(state.clock.getElapsedTime()) * 0.1
      }
    }

    if (progressRef.current && isUploading) {
      progressRef.current.scale.y = progress / 100
    }
  })

  return (
    <group ref={docRef}>
      {/* Document */}
      <RoundedBox args={[2, 2.8, 0.1]} radius={0.05} smoothness={4}>
        <meshStandardMaterial
          color="#ffffff"
          metalness={0.1}
          roughness={0.8}
        />
      </RoundedBox>

      {/* Document lines */}
      {[0.6, 0.3, 0, -0.3, -0.6].map((y, i) => (
        <mesh key={i} position={[0, y, 0.06]}>
          <boxGeometry args={[1.5, 0.05, 0.01]} />
          <meshBasicMaterial color="#94a3b8" />
        </mesh>
      ))}

      {/* File name */}
      <Text
        position={[0, -1.6, 0.06]}
        fontSize={0.15}
        color="#1e293b"
        anchorX="center"
        anchorY="middle"
        maxWidth={1.8}
      >
        {fileName}
      </Text>

      {/* Progress indicator */}
      {isUploading && (
        <group position={[0, 0, 0.2]}>
          {/* Background ring */}
          <mesh rotation={[0, 0, 0]}>
            <torusGeometry args={[1.5, 0.05, 16, 100]} />
            <meshBasicMaterial color="#334155" transparent opacity={0.3} />
          </mesh>

          {/* Progress ring */}
          <mesh ref={progressRef} rotation={[0, 0, -Math.PI / 2]}>
            <torusGeometry args={[1.5, 0.06, 16, 100, Math.PI * 2 * (progress / 100)]} />
            <meshBasicMaterial color="#0ea5e9" />
          </mesh>

          {/* Progress text */}
          <Text
            position={[0, 0, 0]}
            fontSize={0.4}
            color="#0ea5e9"
            anchorX="center"
            anchorY="middle"
          >
            {Math.round(progress)}%
          </Text>
        </group>
      )}

      {/* Success particles */}
      {!isUploading && progress === 100 && (
        <group>
          {Array.from({ length: 20 }).map((_, i) => {
            const angle = (i / 20) * Math.PI * 2
            const radius = 2
            return (
              <mesh
                key={i}
                position={[
                  Math.cos(angle) * radius,
                  Math.sin(angle) * radius,
                  0
                ]}
              >
                <sphereGeometry args={[0.05, 8, 8]} />
                <meshBasicMaterial color="#10b981" />
              </mesh>
            )
          })}
        </group>
      )}
    </group>
  )
}

export default function DocumentPreview3D({
  fileName,
  fileType,
  isUploading = false,
  progress = 0,
  className = ''
}: DocumentPreview3DProps) {
  return (
    <div className={`w-full h-96 ${className}`}>
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[5, 5, 5]} intensity={1} />
        <pointLight position={[-5, -5, -5]} intensity={0.5} color="#8b5cf6" />
        <spotLight position={[0, 10, 0]} angle={0.3} penumbra={1} intensity={1} />

        <Document3D
          fileName={fileName}
          isUploading={isUploading}
          progress={progress}
        />
      </Canvas>
    </div>
  )
}
