import {useState, createContext, useContext, ReactNode, useEffect, useRef, useCallback} from 'react';
import { pythonAuth, pythonCheck, pythonFetchRange } from '../services';
import { useFilter } from './FilterContext';
import { useCartridge } from './CartridgeContext';

interface ControlContextType {
    checkDone: boolean
    setCheckDone: (_: boolean) => void
    isAuthenticating: boolean
    authError: string | null
    forceReauth: () => void
    cartridgeLoading: boolean;
    setCartridgeLoading: (_: boolean) => void
}


interface CartridgeInfo {
  id: number;
  build_date: string;
  build_time: string;
  class_code: string;
  qc_status: string;
  qc_date: string;
  qc_time: string;
  qc_user: string;
}



interface FetchInfo {
  values: CartridgeInfo[];
  prod_start: string;
  prod_end: string;
}


const ControlContext = createContext<ControlContextType | undefined>(undefined)
  
export const useControl = (): ControlContextType => {
    const context = useContext(ControlContext)
    if (!context) {
        throw new Error("useControl must be used within a ControlProvider")
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
    const [cartridgeLoading, setCartridgeLoading] = useState<boolean>(false);
    const { setCartridgeList } = useCartridge()
    const {
        setValidUsers, setValidTypes, qcDateRange,
        setProdDateRange,
    } = useFilter()
    
    const fetchData = useCallback(async () => {
        setCartridgeLoading(true);
        try {
        const raw = await pythonFetchRange(qcDateRange[0], qcDateRange[1]);
        const parsed: FetchInfo = JSON.parse(String(raw));
        const values = parsed["values"]
        const uniqueTypes = [...new Set(values.map(item => Number(item.class_code)))];
        const uniqueUsers = [...new Set(values.map(item => item.qc_user).filter(u => u != null))]
        setValidTypes(uniqueTypes);
        setValidUsers(uniqueUsers)
        setCartridgeList([]);
        setCartridgeList(values);
        setProdDateRange([new Date(parsed.prod_start), new Date(parsed.prod_end)])
        } catch (error) {
        console.error("Error fetching/parsing cartridge list:", error);
        setCartridgeList([]); // Reset on error
        } finally {
        setCartridgeLoading(false);
        }
    }, [qcDateRange[0], qcDateRange[1], setValidTypes]);

    useEffect(() => {
        if (checkDone) {
        fetchData();
        }
    }, [checkDone, fetchData]);


    const authenticate = async (): Promise<boolean> => {
        if (loginInProgress.current) return false
        loginInProgress.current = true
        setIsAuthenticating(true)
        setAuthError(null)

        try {
            let result = await pythonCheck()
            
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
            forceReauth,
            cartridgeLoading,
            setCartridgeLoading
        }}>
            {children}
        </ControlContext.Provider>
    )
};