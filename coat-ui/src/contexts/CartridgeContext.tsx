import {useState, createContext, useContext, ReactNode} from 'react';

interface CartridgeContextType {
  cartridgeList: string[];
  addCartridge: (id: string) => void;
  removeCartridge: (id: string) => void;
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
  const [cartridgeList, setCartridgeList] = useState<string[]>([]);
  
  const addCartridge = (id: string) => {
    setCartridgeList(prev => [...prev, id])
  };
  const removeCartridge = (id: string) => {
    setCartridgeList(prev => prev.filter(c =>  c !== id));
  }

  return (
    <CartridgeContext.Provider value={{ cartridgeList, addCartridge, removeCartridge }}>
      {children}
    </CartridgeContext.Provider>
  );
};