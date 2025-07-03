// import { useState } from "react";
import { Logo } from "./components";
import { useState } from "react";
import { BottomText, CartridgeList, TopContainer, ErrorPopUpContainer, SettingsContainer } from "./containers";
import { CartridgeProvider, DateProvider, PopUpProvider } from "./contexts";
import Modal  from "react-modal"
import "./App.css";

Modal.setAppElement('#root');




function App() {
  const [idFilter, setFilter] = useState<string>("")
  
  return (
    <CartridgeProvider>
    <PopUpProvider>
      <main className="container">
        <ErrorPopUpContainer/>
        <SettingsContainer />
        <Logo/>
        <DateProvider>
          <TopContainer setFilter={setFilter}/>
          <CartridgeList filterText={idFilter}/>
        </DateProvider>
        <BottomText/>
      </main>
    </PopUpProvider>
    </CartridgeProvider>
  );
}

export default App;
