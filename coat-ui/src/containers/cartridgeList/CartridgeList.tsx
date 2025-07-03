import { CartridgeListItem } from "../../components";
import { pythonFetchRange } from "../../services";
import { useEffect, useRef, useState } from "react";
import { pythonAuth, pythonCheck } from "../../services";
import "./cartridgeList.css";
import { useDate } from "../../contexts";

interface CartridgeInfo {
  id: string;
  b_date: string;
}

interface CartridgeListProps {
  filterText: string
}

function CartridgeList({ filterText }: CartridgeListProps) {
  const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);
  const [checkDone, setCheckDone] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const {startDate, endDate} = useDate()
  const loginInProgress = useRef(false);

  useEffect(() => {

    const check = async () => {
      if (loginInProgress.current) return;
      loginInProgress.current = true;
      try {
        let result = await pythonCheck();
        console.log(result)
        while (!result) {
          const user = prompt("Enter username:", "");
          const pass = prompt("Enter passkey:", "");
          if (user === null || pass === null) {
            alert("Login cancelled.");
            loginInProgress.current = false;
            return;
          }
          result = await pythonAuth(user, pass);
        }
        setCheckDone(true);
      } catch (err) {
        console.error("Failed to run python_check:", err);
      } finally {
        loginInProgress.current = false;
      }
    };

    check();
  }, []);

  useEffect(() => {
    if (!checkDone) return;
    const fetchData = async () => {
      setLoading(true)
      try {
        const raw = String(await pythonFetchRange(startDate, endDate)); // returns JSON string
        const parsed: CartridgeInfo[] = JSON.parse(raw);
        setCartridgeList(parsed);
      } catch (error) {
        console.error("Error fetching/parsing cartridge list:", error);
      }
      
      setLoading(false)
    };
    
    fetchData();
  }, [checkDone, startDate, endDate]);

  if (cartridgeList.length == 0 || !checkDone || loading) return <div>Loading Cartridge Data...</div>;

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
