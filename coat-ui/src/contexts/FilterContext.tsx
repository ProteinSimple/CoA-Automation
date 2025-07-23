
import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import chroma from 'chroma-js';


interface FilterContextType {
    showOnlyPassed: boolean;
    setShowOnlyPassed: (_: boolean) => void;
    showProdTime: boolean;
    setShowProdTime: (_: boolean) => void;
    prodDateRange: [Date, Date];
    setProdDateRange: (range: [Date, Date]) => void;
    qcDateRange: [Date, Date]
    setQCDateRange: (_: [Date, Date]) => void
    selectedTypes: number[]
    setTypes: (_: number[]) => void
    validTypes: number[]
    setValidTypes: (_: number[]) => void
    colorMap: Record<number, string>
    selectedUsers: string[]
    setSelectedUsers: (_: string[]) => void
    validUsers: string[]
    setValidUsers: (_: string[]) => void;
    filterText: string;
    setFilterText: (_: string) => void
}


const FilterContext = createContext<FilterContextType | undefined>(undefined)

export const useFilter = () => {
    const context = useContext(FilterContext)
    if (!context) throw new Error("useFilter must be used within a FilterProvider");
    return context
}


interface FilterProviderProps {
  children: ReactNode;
}


export const FilterProvider = ({ children }: FilterProviderProps) => {
  let prev_valid: number[] = []
  const [qcEndDate, setQCEndDate] = useState<Date>(new Date());
  const [qcStartDate, setQCStartDate] = useState<Date>(() => {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    return d;
  });

  const [prodDateRange, setProdDateRange] = useState<[Date, Date]>([qcStartDate, qcEndDate])

  const [selectedTypes, setTypes] = useState<number[]>([]);
  const [validTypes, setValidTypes] = useState<number[]>([]);
  const [selectedUsers, setSelectedUsers] = useState<string[]>([])
  const [validUsers, setValidUsers] = useState<string[]>([])
  const [colorMap, setColorMap] = useState<Record<number, string>>({});
  const [showOnlyPassed, setShowOnlyPassed] = useState<boolean>(true);
  const [showProdTime, setShowProdTime] = useState<boolean>(false);
  const [filterText, setFilterText] = useState<string>("")
  
  
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

  function setQCDateRange(given: [Date, Date]) {
    setQCStartDate(given[0])
    setQCEndDate(given[1])
  }

  return (
    <FilterContext.Provider value={{ 
      // showing only cartridges with QC passed
      showOnlyPassed,
      setShowOnlyPassed,
      // Whether to show prod or QC time
      showProdTime,
      setShowProdTime,
      // Prod Date filter
      prodDateRange,
      setProdDateRange, 
      // QC Date filter
      qcDateRange: [qcStartDate, qcEndDate],
      setQCDateRange,
      // filtering cartridges by their type
      selectedTypes, 
      setTypes, 
      validTypes, 
      setValidTypes,
      // filtering by QC user
      selectedUsers,
      setSelectedUsers,
      validUsers,
      setValidUsers,
      // color map for assigning color. This should be changed!
      colorMap,
      // Filter Text
      filterText,
      setFilterText
    }}>
      {children}
    </FilterContext.Provider>
  );
};