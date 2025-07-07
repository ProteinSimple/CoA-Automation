import { useState, createContext, useContext, ReactNode } from 'react';


interface FilterContextType {
    startDate: Date;
    endDate: Date;
    setStartDate: (_: Date) => void;
    setEndDate: (_: Date) => void;
    selectedTypes: number[]
    setTypes: (_: number[]) => void
    validTypes: number[]
    setValidTypes: (_: number[]) => void
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
  const [endDate, setEndDate] = useState<Date>(new Date());
  const [startDate, setStartDate] = useState<Date>(() => {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    return d;
  });

  const [selectedTypes, setTypes] = useState<number[]>([])
  const [validTypes, setValidTypes] = useState<number[]>([])

  return (
    <FilterContext.Provider value={{ startDate, endDate, setStartDate, setEndDate, selectedTypes, setTypes, validTypes, setValidTypes }}>
      {children}
    </FilterContext.Provider>
  );
};