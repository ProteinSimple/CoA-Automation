import { CartridgeListItem } from "../../components";
import { pythonFetchIds } from "../../services";
import { useEffect, useState } from "react";
import "./cartridgeList.css"


interface CartridgeInfo {
  id: string;
  b_date: string;
}

interface CartridgeListProps {
  checkDone: boolean;
  add: (newCartridge: string) => void;
  remove: (given: string) => void;
  filterText: string
}

function CartridgeList({ checkDone, add, remove, filterText } : CartridgeListProps) {    
    const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);

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

    // const filteredList = useMemo(() => {
    //     return cartridgeList.filter(d =>
    //     d.id.toLowerCase().includes(filterText.toLowerCase())
    //     );
    // }, [cartridgeList, filterText]);

    return (
        <div className="list_container">
            {cartridgeList.map(d =>
                d.id.toLowerCase().includes(filterText.toLowerCase()) ? (
                    <CartridgeListItem
                    key={d.id}
                    id={d.id}
                    time={d.b_date}
                    add={add}
                    remove={remove}
                    />
                ) : null
            )}
        </div>
    )
}

export default CartridgeList;