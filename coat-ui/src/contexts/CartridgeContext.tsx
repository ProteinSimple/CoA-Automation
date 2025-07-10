import {useState, createContext, useContext, ReactNode} from 'react';

interface CartridgeContextType {
  selectedCartridgeList: Set<string>;
  addCartridge: (id: string) => void;
  removeCartridge: (id: string) => void;
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
  const [cartridgeList, setCartridgeList] = useState<Set<string>>(new Set());
  
  const addCartridge = (id: string) => {
    setCartridgeList(prev => new Set(prev).add(id))
  };
  const removeCartridge = (id: string) => {
    const s = new Set(cartridgeList)
    s.delete(id)
    setCartridgeList(s)
  }

  const  clearSelected = () => {
    const s = new Set(cartridgeList)
    s.clear()
    setCartridgeList(s)
  }

  return (
    <CartridgeContext.Provider value={{ selectedCartridgeList: cartridgeList, addCartridge, removeCartridge, clearSelected }}>
      {children}
    </CartridgeContext.Provider>
  );
};