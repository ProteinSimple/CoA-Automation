// import { useState } from "react";
import { Logo } from "./components";
import { useState } from "react";
import { BottomText, CartridgeList, TopContainer } from "./containers";
import { CartridgeProvider } from "./contexts";
import "./App.css";


function App() {
  const [idFilter, setFilter] = useState<string>("")

  return (
    <CartridgeProvider>
      <main className="container">
        <Logo/>
        <TopContainer setFilter={setFilter}/>
        <CartridgeList filterText={idFilter}/>
        <BottomText/>
      </main>
    </CartridgeProvider>
  );
}

export default App;
