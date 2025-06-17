import { CartridgeListItem } from "../../components";
import { pythonListIds } from "../../services";
import { useEffect, useState } from "react";
import "./cartridgeList.css"


interface CartridgeInfo {
  id: string;
  b_date: string;
}

function CartridgeList() {    
    const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);

    useEffect(() => {
        const fetchData = async () => {
        try {
            const raw = String(await pythonListIds()); // returns JSON string
            const parsed: CartridgeInfo[] = JSON.parse(raw);
            setCartridgeList(parsed); 
        } catch (error) {
            console.error("Error fetching/parsing cartridge list:", error);
        }
        };

        fetchData();
    }, []);
    return (
        <div className="list_container">
            {cartridgeList.map(d => <CartridgeListItem id={d.id} time={d.b_date}></CartridgeListItem>)}
        </div>
    )
}

export default CartridgeList;