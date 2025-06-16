// import { useState } from "react";
import logo from "./assets/ProteinSimple-horiz-white.png";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";

type ListItemProps = {
  id: string;
  time: string;
  date: string;
};

type CheckboxProps = {
  id: string;
}

function Checkbox ({ id } : CheckboxProps) {
  return (
    <label className="checkbox-wrapper"
           id={id}>
    <input type="checkbox" />
    <span className="custom-checkbox"></span>
    </label>
  )
}

function ListItem( { id, time, date }: ListItemProps) {
  return (
    <div className="list_item">
      <Checkbox id={id}>
      </Checkbox>
      <p>
        {id}
      </p> 
      <p className="list_item_date">
        {time}  {date}  
      </p> 
    </div>
    
  )
}


function App() {
  const datas = [
    {SN: "SN1", time: "12:00" ,man_date: "21/04/2025", exp_date : "30/05/2025"},
    {SN: "SN2", time: "12:00" ,man_date: "22/04/2025", exp_date : "01/06/2025"},
    {SN: "SN3", time: "12:00" ,man_date: "23/04/2025", exp_date : "02/06/2025"},
  ]
  async function greet() {
    let mes = await invoke("python_com", {})
    console.log(mes)
  }

  return (
    <main className="container">
      <div>
        <img src={logo} alt="logo-placeholder" className="logo" />
      </div>
      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          greet();
        }}
      >
        <input
          id="SN-search"
          placeholder="Search 🔍"
        />
        <input
          id="greet-input"
          placeholder="Enter a name..."
        />
        <button type="submit">Greet</button>
      </form>
      <div className="list_container">
        {datas.map(d => <ListItem id={d.SN} time={d.time} date={d.man_date}></ListItem>)}
      </div>
    </main>
  );
}

export default App;
