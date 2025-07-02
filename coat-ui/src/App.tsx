// import { useState } from "react";
import { Logo } from "./components";
import { useState } from "react";
import { BottomText, CartridgeList, TopContainer, ErrorPopUpContainer, SettingsContainer } from "./containers";
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
  const [ setting, setSetting] = useState<boolean>(false);
  const showSettings = () => { setSetting(true) }
  const hideSettings = () => { setSetting(false) }

  return (
    <CartridgeProvider>
      <main className="container">
        <ErrorPopUpContainer errorTup={error} setError={setError}/>
        <SettingsContainer isOpen={setting} onClose={hideSettings}/>
        <Logo CogAction={showSettings}/>
        <TopContainer setFilter={setFilter} setError={setError} setStart={setStart} setEnd={setEnd} startDate={startDate} endDate={endDate}/>
        <CartridgeList filterText={idFilter} startDate={startDate} endDate={endDate}/>
        <BottomText/>
      </main>
    </CartridgeProvider>
  );
}

export default App;
