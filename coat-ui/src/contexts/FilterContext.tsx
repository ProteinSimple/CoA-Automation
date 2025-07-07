import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import chroma from 'chroma-js';


interface FilterContextType {
    startDate: Date;
    endDate: Date;
    setStartDate: (_: Date) => void;
    setEndDate: (_: Date) => void;
    selectedTypes: number[]
    setTypes: (_: number[]) => void
    validTypes: number[]
    setValidTypes: (_: number[]) => void
    colorMap: Record<number, string>
}


const FilterContext = createContext<FilterContextType | undefined>(undefined)

export const useFilter = () => {
    const context = useContext(FilterContext)
    if (!context) throw new Error("useDate must be used within a DateProvider");
    return context
}


interface FilterProviderProps {
  children: ReactNode;
}


export const FilterProvider = ({ children }: FilterProviderProps) => {
  let prev_valid: number[] = []
  const [endDate, setEndDate] = useState<Date>(new Date());
  const [startDate, setStartDate] = useState<Date>(() => {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    return d;
  });

  const [selectedTypes, setTypes] = useState<number[]>([])
  const [validTypes, setValidTypes] = useState<number[]>([])
  const [colorMap, setColorMap] = useState<Record<number, string>>({});
  
  useEffect(() => {
    if (prev_valid === validTypes) {
      return
    }
    prev_valid = structuredClone(validTypes)
    if (validTypes.length === 0) {
      setColorMap({});
      return;
    }
    const colors = chroma.scale('Set3').mode('lch').colors(validTypes.length);
    const newColorMap: Record<number, string> = {};
    validTypes.forEach((type, idx) => { newColorMap[type] = colors[idx] });
    setColorMap(newColorMap);
  }, [validTypes]);



  return (
    <FilterContext.Provider value={{ 
      startDate,
      endDate,
      setStartDate, 
      setEndDate, 
      selectedTypes, 
      setTypes, 
      validTypes, 
      setValidTypes,
      colorMap
    }}>
      {children}
    </FilterContext.Provider>
  );
};