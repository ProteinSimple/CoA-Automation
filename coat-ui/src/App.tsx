// import { useState } from "react";
import { Logo } from "./components";
import { useEffect, useState } from "react";
import { pythonAuth, pythonCheck } from "./services";
import { BottomText, CartridgeList, TopContainer } from "./containers";
import "./App.css";


function App() {
  const [checkDone, setCheckDone] = useState<boolean>(false);
  const [selectedCart, setSelectCart] = useState<string[]>([])
  const [idFilter, setFilter] = useState<string>("")

  const addCartridge = (newCartridge: string) => {
    setSelectCart(prev => [...prev, newCartridge]);
  };

  const removeCartridge = (remove: string) => {
    setSelectCart(prev => prev.filter(id => id !== remove));
  };

  useEffect(() => {
    const check = async () => {
      try {
        let result = await pythonCheck();
        console.log("python_check result:", result);

        while(!result) {
          const user = prompt("Enter username:", "");
          const pass = prompt("Enter passkey:", "");
          try {
            result = await pythonAuth(user, pass);
          } catch (err) {
            console.error("Auth error:", err);
            alert("An error occurred. Try again.");
          }
        }
        setCheckDone(true)
      } catch (err) {
        console.error("Failed to run python_check:", err);
      }
    };
    
    check();
  }, []);

  return (
    <main className="container">
      <div>
        <Logo/>
      </div>
      <TopContainer setFilter={setFilter} selected={selectedCart}/>
      <CartridgeList filterText={idFilter} add={addCartridge} remove={removeCartridge} checkDone={checkDone}/>
      <BottomText/>
    </main>
  );
}

export default App;
