import { useState, createContext, useContext, ReactNode, useEffect } from 'react';
import { GenericContextProviderProps } from './shared';
import { pythonConfigAddMapping, pythonConfigAddPdf, pythonConfigDeleteMapping, pythonConfigDeletePdf, pythonConfigList } from '../services';
import { useControl } from './ControlContext';
import { usePopUp } from './PopUpContext';


interface SettingsContextType {
    pdfPaths: string[];
    addPdfPath: (_: string) => void;
    removePdfPath: (_: string) => void;
    mappingPaths: string[];
    addMappingPath: (_: string) => void;
    removeMappingPath: (_: string) => void;
}

const SettingsContext = createContext<SettingsContextType | undefined>(undefined)

export const useSettings = () => {
    const context = useContext(SettingsContext)
    if (!context) throw new Error("useSettings must be used within a DateProvider");
    return context
}

export const SettingsProvider = ({ children }: GenericContextProviderProps) => {

    
    const { setting: isOpen} = usePopUp()
    const { checkDone } = useControl();
    
    const [pdfPaths, setPdfPaths] = useState<string[]>([])
    const [mappingPaths, setMappingPaths] = useState<string[]>([])

    const addPdfPath = async (given: string) => {
      try {
          const res = await pythonConfigAddPdf([given])
          const config = JSON.parse(res as string) as { [key: string]: any }
          setPdfPaths(config["pdf_output_dir"])
      } catch (err) {
          console.error("Failed to fetch or parse config:", err);
      }
    }
  
    
  
    const removePdfPath = async (given: string) => {
      try {
          const res = await pythonConfigDeletePdf([given])
          const config = JSON.parse(res as string) as { [key: string]: any }
          setPdfPaths(config["pdf_output_dir"])
      } catch (err) {
          console.error("Failed to fetch or parse config:", err);
      }
    }
  
    const addMappingPath = async (given: string) => {
      try {
          const res = await pythonConfigAddMapping([given])
          const config = JSON.parse(res as string) as { [key: string]: any }
          setMappingPaths(config["mapping_output_dir"])
      } catch (err) {
          console.error("Failed to fetch or parse config:", err);
      }
    }
  
    const removeMappingPath = async (given: string) => {
      try {
          const res = await pythonConfigDeleteMapping([given])
          const config = JSON.parse(res as string) as { [key: string]: any }
          setMappingPaths(config["mapping_output_dir"])
      } catch (err) {
          console.error("Failed to fetch or parse config:", err);
      }
    }
  
    useEffect(() => {
      const effect = async () => {
        if (!checkDone) return
        try {
          const res = await pythonConfigList();
          const config = JSON.parse(res as string) as { [key: string]: any };
          setPdfPaths(config["pdf_output_dir"]);
          setMappingPaths(config["mapping_output_dir"]);
        } catch (err) {
          console.error("Failed to fetch or parse config:", err);
        }
      }
      effect()
    }, [isOpen, checkDone])
    

  return (
    <SettingsContext.Provider value={{ 
        pdfPaths, addPdfPath, removePdfPath,
        mappingPaths, addMappingPath, removeMappingPath
     }}>
        {children}
    </SettingsContext.Provider>
  );
};