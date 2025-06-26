import { CartridgeListItem } from "../../components";
import { pythonFetchIds } from "../../services";
import { useEffect, useState } from "react";
import { pythonAuth, pythonCheck } from "../../services";
import "./cartridgeList.css";

interface CartridgeInfo {
  id: string;
  b_date: string;
}

interface CartridgeListProps {
  filterText: string;
}

function CartridgeList({ filterText }: CartridgeListProps) {
  const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);
  const [checkDone, setCheckDone] = useState<boolean>(false);

  useEffect(() => {
    const check = async () => {
      try {
        let result = await pythonCheck();
        while (!result) {
          const user = prompt("Enter username:", "");
          const pass = prompt("Enter passkey:", "");
          if (user === null || pass === null) {
            alert("Login cancelled.");
            break;
          }
          result = await pythonAuth(user, pass);
        }
        setCheckDone(true);
      } catch (err) {
        console.error("Failed to run python_check:", err);
      }
    };

    check();
  }, []);

  useEffect(() => {
    if (!checkDone) return;
    const fetchData = async () => {
      try {
        const raw = String(await pythonFetchIds()); // returns JSON string
        const parsed: CartridgeInfo[] = JSON.parse(raw);
        setCartridgeList(parsed);
      } catch (error) {
        console.error("Error fetching/parsing cartridge list:", error);
      }
    };

    fetchData();
  }, [checkDone]);

  if (cartridgeList.length == 0) return <div>Loading Cartridge Data...</div>;

  const filteredList = cartridgeList.filter((d) =>
    d.id.toLowerCase().includes(filterText.toLowerCase())
  );

  return (
    <div className="list_container">
      {filteredList.map((d) => (
        <CartridgeListItem key={d.id} id={d.id} time={d.b_date} />
      ))}
    </div>
  );
}

export default CartridgeList;
