import { useState, createContext, useContext, ReactNode, useMemo} from 'react';
import { useFilter } from './FilterContext';

interface CartridgeInfo {
  id: number;
  build_date: string;
  build_time: string;
  class_code: string;
  qc_status: string;
  qc_date: string;
  qc_time: string;
  qc_user: string;
  color: string;
}

interface CartridgeContextType {
  cartridgeList: CartridgeInfo[];
  setCartridgeList: (_: CartridgeInfo[]) => void;
  filteredList: CartridgeInfo[];
  selectedCartridgeList: Set<number>;
  addSelectedCartridge: (id: number) => void;
  removeSelectedCartridge: (id: number) => void;
  clearSelected: () => void
}



const CartridgeContext = createContext<CartridgeContextType | undefined>(undefined)
  
export const useCartridge = (): CartridgeContextType => {
    const context = useContext(CartridgeContext)
    if (!context) {
        throw new Error("useCartridge must be used within a CartridgeProvider")
    }
    return context
}

interface CartridgeProviderProps {
  children: ReactNode;
}


export const CartridgeProvider = ({ children }: CartridgeProviderProps) => {
  
  const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);
  const [selectedCartridgeList, setSelectedCartridgeList] = useState<Set<number>>(new Set());  

  const {
      prodDateRange, selectedTypes, selectedUsers,
       showOnlyPassed, filterText
  } = useFilter()


  const filteredList = useMemo(() => {
    if (!cartridgeList.length) return [];
    const lowerFilterText = filterText.toLowerCase();
    
    return cartridgeList.filter((item) => {
      const id_str = String(item.id)
      const matchesFilter = id_str.toLowerCase().includes(lowerFilterText);
      const matchesType = selectedTypes.length === 0 || selectedTypes.includes(Number(item.class_code));
      const matchesUser = selectedUsers.length === 0 || selectedUsers.includes(item.qc_user);
      const passedQc = !showOnlyPassed || item.qc_status === "P"

      return matchesFilter && matchesType && matchesUser && passedQc;
    });
  }, [cartridgeList, filterText, selectedTypes, showOnlyPassed, prodDateRange, selectedUsers]);

  
    
  const addSelectedCartridge = (id: number) => {
    setSelectedCartridgeList(prev => new Set(prev).add(id))
  };
  const removeSelectedCartridge = (id: number) => {
    const s = new Set(selectedCartridgeList)
    s.delete(id)
    setSelectedCartridgeList(s)
  }

  const  clearSelected = () => {
    const s = new Set(selectedCartridgeList)
    s.clear()
    setSelectedCartridgeList(s)
  }

  return (
    <CartridgeContext.Provider value={
      {
        cartridgeList,
        setCartridgeList,
        filteredList, 
        selectedCartridgeList,
        addSelectedCartridge,
        removeSelectedCartridge,
        clearSelected
      }}>
       {children}
    </CartridgeContext.Provider>
  );
};