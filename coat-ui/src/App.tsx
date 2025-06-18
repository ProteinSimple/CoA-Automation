// import { useState } from "react";
import { Logo } from "./components";
import { BottomText, CartridgeList, TopContainer } from "./containers";
import "./App.css";




function App() {

  return (
    <main className="container">
      <Logo/>
      <TopContainer/>
      <CartridgeList/>
      <BottomText/>
    </main>
  );
}

export default App;
