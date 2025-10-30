import { Link, useLocation } from 'react-router-dom'
import { Upload, CheckCircle, Database, Activity, Home, Mail } from 'lucide-react'
import { ReactNode, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ThemeToggle from './ThemeToggle'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const [hoveredItem, setHoveredItem] = useState<string | null>(null)
  
  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/dashboard', label: 'Dashboard', icon: Activity },
    { path: '/verify', label: 'Verify Documents', icon: CheckCircle },
    { path: '/upload', label: 'Upload Document', icon: Upload },
    { path: '/records', label: 'Records', icon: Database },
    { path: '/email-watcher', label: 'Email Watcher', icon: Mail },
  ]
  
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors">
      <motion.header 
        className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50 transition-colors"
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <motion.div 
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
            >
              {/* Logo */}
              <motion.div 
                className="relative w-10 h-10"
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <div className="absolute inset-0 flex items-end justify-center space-x-0.5">
                  <motion.div 
                    className="w-2 bg-gradient-to-t from-amber-600 to-amber-400 rounded-t" 
                    style={{ height: '40%' }}
                    animate={{ height: ['40%', '50%', '40%'] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                  />
                  <motion.div 
                    className="w-2 bg-gradient-to-t from-amber-600 to-amber-400 rounded-t" 
                    style={{ height: '60%' }}
                    animate={{ height: ['60%', '70%', '60%'] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.2 }}
                  />
                  <motion.div 
                    className="w-2 bg-gradient-to-t from-amber-600 to-amber-400 rounded-t" 
                    style={{ height: '80%' }}
                    animate={{ height: ['80%', '90%', '80%'] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.4 }}
                  />
                </div>
                <motion.div 
                  className="absolute -top-1 -right-1 w-4 h-4 text-amber-600"
                  animate={{ rotate: [0, 10, -10, 0] }}
                  transition={{ duration: 3, repeat: Infinity }}
                >
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M7 17L17 7M17 7H7M17 7V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                  </svg>
                </motion.div>
              </motion.div>
              <div>
                <motion.h1 
                  className="text-xl font-bold bg-gradient-to-r from-amber-600 to-amber-800 dark:from-amber-400 dark:to-amber-600 bg-clip-text text-transparent"
                  whileHover={{ scale: 1.05 }}
                >
                  FinsightAI
                </motion.h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">Invoice Verification System</p>
              </div>
            </motion.div>
            
            <div className="flex items-center space-x-4">
              <nav className="hidden md:flex space-x-1">
                {navItems.map((item, idx) => {
                  const Icon = item.icon
                  const isActive = location.pathname === item.path
                  const isHovered = hoveredItem === item.path
                  
                  return (
                    <motion.div
                      key={item.path}
                      initial={{ opacity: 0, y: -20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.1, type: "spring", stiffness: 100 }}
                      onHoverStart={() => setHoveredItem(item.path)}
                      onHoverEnd={() => setHoveredItem(null)}
                    >
                      <Link
                        to={item.path}
                        className="relative flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors"
                      >
                        <motion.div
                          animate={isHovered ? { rotate: [0, -10, 10, 0], scale: [1, 1.2, 1.2, 1] } : {}}
                          transition={{ duration: 0.5 }}
                        >
                          <Icon className={`w-4 h-4 ${
                            isActive
                              ? 'text-amber-700 dark:text-amber-400'
                              : 'text-gray-600 dark:text-gray-300'
                          }`} />
                        </motion.div>
                        <span className={`font-medium ${
                          isActive
                            ? 'text-amber-700 dark:text-amber-400'
                            : 'text-gray-600 dark:text-gray-300'
                        }`}>
                          {item.label}
                        </span>
                        
                        {/* Active indicator */}
                        {isActive && (
                          <motion.div
                            className="absolute inset-0 bg-amber-50 dark:bg-amber-900/20 rounded-lg -z-10"
                            layoutId="activeTab"
                            transition={{ type: "spring", stiffness: 300, damping: 30 }}
                          />
                        )}
                        
                        {/* Hover effect */}
                        {!isActive && isHovered && (
                          <motion.div
                            className="absolute inset-0 bg-gray-50 dark:bg-gray-700 rounded-lg -z-10"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                          />
                        )}
                        
                        {/* Bottom border animation */}
                        <motion.div
                          className="absolute bottom-0 left-0 right-0 h-0.5 bg-amber-600 dark:bg-amber-400"
                          initial={{ scaleX: 0 }}
                          animate={{ scaleX: isActive ? 1 : 0 }}
                          transition={{ duration: 0.3 }}
                        />
                      </Link>
                    </motion.div>
                  )
                })}
              </nav>
              <motion.div
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5, type: "spring", stiffness: 200 }}
              >
                <ThemeToggle />
              </motion.div>
            </div>
          </div>
        </div>
      </motion.header>
      
      <motion.main 
        className="flex-1"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </div>
      </motion.main>
      
      <motion.footer 
        className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-auto transition-colors"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <motion.p 
            className="text-center text-sm text-gray-500 dark:text-gray-400"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            © 2025 FinsightAI. Invoice & Purchase Order Verification System.
          </motion.p>
        </div>
      </motion.footer>
    </div>
  )
}
