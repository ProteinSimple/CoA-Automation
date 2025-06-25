// import { useState } from "react";
import { Logo } from "./components";
import { useState } from "react";
import { BottomText, CartridgeList, TopContainer, ErrorPopUpContainer } from "./containers";
import { CartridgeProvider } from "./contexts";
import Modal  from "react-modal"
import "./App.css";

Modal.setAppElement('#root');



function App() {
  const [idFilter, setFilter] = useState<string>("")
  const [error, setError] = useState<[boolean, string]>([false, ""]);
  return (
    <CartridgeProvider>
      <main className="container">
        <ErrorPopUpContainer errorTup={error} setError={setError}/>
        <Logo/>
        <TopContainer setFilter={setFilter} setError={setError}/>
        <CartridgeList filterText={idFilter}/>
        <BottomText/>
      </main>
    </CartridgeProvider>
  );
}

export default App;
