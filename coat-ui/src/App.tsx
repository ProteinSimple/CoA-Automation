// import { useState } from "react";
import { Logo } from "./components";
import { CartridgeList, TopContainer } from "./containers";
import "./App.css";




function App() {
  const catridgeData = [
    {SN: "SN1", time: "12:00" ,man_date: "21/04/2025", exp_date : "30/05/2025"},
    {SN: "SN2", time: "12:00" ,man_date: "22/04/2025", exp_date : "01/06/2025"},
    {SN: "SN3", time: "12:00" ,man_date: "23/04/2025", exp_date : "02/06/2025"},
  ]
  

  return (
    <main className="container">
      <Logo/>
      <TopContainer/>
      <CartridgeList data={catridgeData}/>
    </main>
  );
}

export default App;
