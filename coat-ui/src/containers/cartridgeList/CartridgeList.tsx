import { CartridgeListItem } from "../../components";
import { pythonFetchRange } from "../../services";
import { useEffect, useState, useMemo, useCallback } from "react";
import "./cartridgeList.css";
import { useControl, useFilter } from "../../contexts";

interface CartridgeInfo {
  id: string;
  b_date: string;
  type: string;
}

interface CartridgeListProps {
  filterText: string
}

function CartridgeList({ filterText }: CartridgeListProps) {
  const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);
  const [loading, setLoading] = useState<boolean>(false);


  const { checkDone } = useControl();
  const {startDate, endDate, selectedTypes, setValidTypes } = useFilter()

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const raw = await pythonFetchRange(startDate, endDate);
      const parsed: CartridgeInfo[] = JSON.parse(String(raw));
      const uniqueTypes = [...new Set(parsed.map(item => Number(item.type)))];
      setValidTypes(uniqueTypes);
      setCartridgeList(parsed);
    } catch (error) {
      console.error("Error fetching/parsing cartridge list:", error);
      setCartridgeList([]); // Reset on error
    } finally {
      setLoading(false);
    }
  }, [startDate, endDate, setValidTypes]);


  useEffect(() => {
    if (checkDone) {
      fetchData();
    }
  }, [checkDone, fetchData]);


  const filteredList = useMemo(() => {
    if (!cartridgeList.length) return [];
    
    const lowerFilterText = filterText.toLowerCase();
    
    return cartridgeList.filter((item) => {
      const matchesFilter = item.id.toLowerCase().includes(lowerFilterText);
      const matchesType = selectedTypes.length === 0 || selectedTypes.includes(Number(item.type));
      return matchesFilter && matchesType;
    });
  }, [cartridgeList, filterText, selectedTypes]);

  if (!checkDone || loading) { return <div>Loading Cartridge Data...</div>;}

  if (cartridgeList.length === 0) { return <div>No cartridge data available.</div>;}

  if (filteredList.length === 0) { return <div>No cartridges match your current filters.</div>; }

  return (
    <div className="list_container">
      {filteredList.map((d) => (
        <CartridgeListItem key={d.id} id={d.id} time={d.b_date} type={d.type} />
      ))}
    </div>
  );
}

export default CartridgeList;
