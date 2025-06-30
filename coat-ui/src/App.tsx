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
  const [endDate, setEnd] = useState<Date>(new Date());
  const [startDate, setStart] = useState<Date>(() => {
    const d = new Date();
    d.setDate(d.getDate() - 1);
    return d;
});
  return (
    <CartridgeProvider>
      <main className="container">
        <ErrorPopUpContainer errorTup={error} setError={setError}/>
        <Logo/>
        <TopContainer setFilter={setFilter} setError={setError} setStart={setStart} setEnd={setEnd} startDate={startDate} endDate={endDate}/>
        <CartridgeList filterText={idFilter} startDate={startDate} endDate={endDate}/>
        <BottomText/>
      </main>
    </CartridgeProvider>
  );
}

export default App;
