
import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import chroma from 'chroma-js';


interface FilterContextType {
    
    showOnlyPassed: boolean;
    setShowOnlyPassed: (_: boolean) => void;
    showProdTime: boolean;
    setShowProdTime: (_: boolean) => void;
    prodStartDate: Date;
    prodEndDate: Date;
    setProdStartDate: (_: Date) => void;
    setProdEndDate: (_: Date) => void;
    qcDateRange: [Date, Date]
    setQCDateRange: (_: [Date, Date]) => void
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
  const [prodEndDate, setProdEndDate] = useState<Date>(new Date());
  const [prodStartDate, setProdStartDate] = useState<Date>(() => {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    return d;
  });

  const [qcDateRange, setQCDateRange] = useState<[Date, Date]>([prodStartDate, prodEndDate])

  const [selectedTypes, setTypes] = useState<number[]>([]);
  const [validTypes, setValidTypes] = useState<number[]>([]);
  const [colorMap, setColorMap] = useState<Record<number, string>>({});
  const [showOnlyPassed, setShowOnlyPassed] = useState<boolean>(true);
  const [showProdTime, setShowProdTime] = useState<boolean>(false);
  
  
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

  useEffect(() =>{
    setQCDateRange([prodStartDate, prodEndDate])
  }, [prodEndDate, prodStartDate])



  return (
    <FilterContext.Provider value={{ 
      // showing only cartridges with QC passed
      showOnlyPassed,
      setShowOnlyPassed,
      // Whether to show prod or QC time
      showProdTime,
      setShowProdTime,
      // Prod Date filter
      prodStartDate,
      prodEndDate,
      setProdStartDate, 
      setProdEndDate, 
      // QC Date filter
      qcDateRange,
      setQCDateRange,
      // filtering cartridges by their type
      selectedTypes, 
      setTypes, 
      validTypes, 
      setValidTypes,
      // color map for assigning color. This should be changed!
      colorMap
    }}>
      {children}
    </FilterContext.Provider>
  );
};