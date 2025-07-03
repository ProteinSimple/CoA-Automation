import { useState, createContext, useContext, ReactNode } from 'react';


interface DateContextType {
    startDate: Date;
    endDate: Date;
    setStartDate: (_: Date) => void;
    setEndDate: (_: Date) => void;
}


const DateContext = createContext<DateContextType | undefined>(undefined)

export const useDate = () => {
    const context = useContext(DateContext)
    if (!context) throw new Error("useDate must be used within a DateProvider");
    return context
}


interface CartridgeProviderProps {
  children: ReactNode;
}


export const DateProvider = ({ children }: CartridgeProviderProps) => {
  const [endDate, setEndDate] = useState<Date>(new Date());
  const [startDate, setStartDate] = useState<Date>(() => {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    return d;
  });

  return (
    <DateContext.Provider value={{ startDate, endDate, setStartDate, setEndDate }}>
      {children}
    </DateContext.Provider>
  );
};