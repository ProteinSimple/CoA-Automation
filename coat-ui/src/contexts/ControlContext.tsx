import {useState, createContext, useContext, ReactNode, useEffect, useRef} from 'react';
import { pythonAuth, pythonCheck } from '../services';

interface ControlContextType {
    checkDone: boolean
    setCheckDone: (_: boolean) => void
    isAuthenticating: boolean
    authError: string | null
    forceReauth: () => void
}

const ControlContext = createContext<ControlContextType | undefined>(undefined)
  
export const useControl = (): ControlContextType => {
    const context = useContext(ControlContext)
    if (!context) {
        throw new Error("useCartridge must be used within a CartridgeProvider")
    }
    return context
}

interface ControlProviderProps {
  children: ReactNode;
}


export const ControlProvider = ({ children }: ControlProviderProps) => {
   const [checkDone, setCheckDone] = useState<boolean>(false)
    const [isAuthenticating, setIsAuthenticating] = useState<boolean>(false)
    const [authError, setAuthError] = useState<string | null>(null)
    const loginInProgress = useRef(false)

    const authenticate = async (): Promise<boolean> => {
        if (loginInProgress.current) return false
        loginInProgress.current = true
        setIsAuthenticating(true)
        setAuthError(null)

        try {
            console.log("About to call pythonCheck()...")
            let result = await pythonCheck()
            console.log("pythonCheck() returned:", result)
            console.log("Type of result:", typeof result)
            console.log("Result === true:", result === true)
            console.log("Result == true:", result == true)
            console.log("Boolean(result):", Boolean(result))
            
            while (!result) {
                const user = prompt("Enter username:", "")
                const pass = prompt("Enter passkey:", "")
                
                if (user === null || pass === null) {
                    setAuthError("Login cancelled by user")
                    return false
                }
                
                result = await pythonAuth(user, pass)
                if (!result) {
                    setAuthError("Invalid credentials, please try again")
                    // Continue the loop to prompt again
                }
            }
            
            setCheckDone(true)
            return true
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : "Authentication failed"
            setAuthError(errorMessage)
            console.error("Failed to run python_check:", err)
            return false
        } finally {
            loginInProgress.current = false
            setIsAuthenticating(false)
        }
    }

    const forceReauth = () => {
        setCheckDone(false)
        setAuthError(null)
        authenticate()
    }

    // Auto-authenticate on mount
    useEffect(() => {
        authenticate()
    }, [])

    return (
        <ControlContext.Provider value={{ 
            checkDone, 
            setCheckDone, 
            isAuthenticating, 
            authError, 
            forceReauth 
        }}>
            {children}
        </ControlContext.Provider>
    )
};