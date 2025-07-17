// import { useState } from "react";
import { Logo } from "./components";
import { useState } from "react";
import { BottomText, CartridgeList, TopContainer, ErrorPopUpContainer, SettingsContainer } from "./containers";
import { CartridgeProvider, ControlProvider, FilterProvider, PopUpProvider } from "./contexts";
import Modal  from "react-modal"
import "./App.css";

Modal.setAppElement('#root');




function App() {
  const [idFilter, setFilter] = useState<string>("")
  
  return (
    <CartridgeProvider>
    <PopUpProvider>
    <ControlProvider>
      <main className="container">
        <ErrorPopUpContainer/>
        
        <Logo/>
        <FilterProvider>
          <SettingsContainer />
          <TopContainer setFilter={setFilter}/>
          <CartridgeList filterText={idFilter}/>
        </FilterProvider>
        <BottomText/>
      </main>
    </ControlProvider>
    </PopUpProvider>
    </CartridgeProvider>
  );
}

export default App;
