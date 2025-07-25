// import { useState } from "react";
import { Logo } from "./components";
import { BottomText, CartridgeList, TopContainer, ErrorPopUpContainer, SettingsContainer } from "./containers";
import { CartridgeProvider, ControlProvider, FilterProvider, PopUpProvider } from "./contexts";
import Modal  from "react-modal"
import "./App.css";

Modal.setAppElement('#root');




function App() {
  return (
    
    <FilterProvider>
    <CartridgeProvider>
    <PopUpProvider>
    <ControlProvider>
      <main className="container">
        <ErrorPopUpContainer/>
        <Logo/>
          <SettingsContainer />
          <TopContainer/>
          <CartridgeList/>
        <BottomText/>
      </main>
    </ControlProvider>
    </PopUpProvider>
    </CartridgeProvider>
    </FilterProvider>
  );
}

export default App;
