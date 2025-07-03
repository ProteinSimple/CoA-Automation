import { useState, createContext, useContext, ReactNode } from 'react';


interface PopUpContextType {
    error: [boolean, string]
    setting: boolean
    showSettings: () => void
    hideSettings: () => void
    setError: (_: [boolean, string]) => void
}

// const [error, setError] = useState<[boolean, string]>([false, ""]);
//   const [ setting, setSetting] = useState<boolean>(false);
//   const showSettings = () => { setSetting(true) }
//   const hideSettings = () => { setSetting(false) }


const PopUpContext = createContext<PopUpContextType | undefined>(undefined)

export const usePopUp = () => {
    const context = useContext(PopUpContext)
    if (!context) throw new Error("useDate must be used within a DateProvider");
    return context
}


interface PopUpProviderProps {
  children: ReactNode;
}


export const PopUpProvider = ({ children }: PopUpProviderProps) => {
  const [error, setError] = useState<[boolean, string]>([false, ""]);
  const [ setting, setSetting] = useState<boolean>(false);
  const showSettings = () => { setSetting(true) }
  const hideSettings = () => { setSetting(false) }
    

  return (
    <PopUpContext.Provider value={{ error, setting, showSettings, hideSettings, setError }}>
      {children}
    </PopUpContext.Provider>
  );
};