import { CartridgeListItem } from "../../components";
import { pythonFetchRange } from "../../services";
import { useEffect, useState, useMemo, useCallback } from "react";
import "./cartridgeList.css";
import { useCartridge, useControl, useFilter } from "../../contexts";

interface CartridgeInfo {
  id: number;
  b_date: string;
  b_time: string;
  type: string;
  passed_qc: string
}

interface CartridgeListProps {
  filterText: string
}

function CartridgeList({ filterText }: CartridgeListProps) {
  const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const { addCartridge, clearSelected, selectedCartridgeList } = useCartridge()
  const { checkDone } = useControl();
  const {startDate, endDate, selectedTypes, setValidTypes, showOnlyPassed } = useFilter()
  const [selectAll, setSelectAll] = useState<boolean>(true)

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const raw = await pythonFetchRange(startDate, endDate);
      const parsed: CartridgeInfo[] = JSON.parse(String(raw));
      const uniqueTypes = [...new Set(parsed.map(item => Number(item.type)))];
      setValidTypes(uniqueTypes);
      setCartridgeList([])
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

  const handleSelectAll = () => {
    if(selectAll) {
      setSelectAll(false)
      filteredList.map(v => addCartridge(v.id))
    } else {
      setSelectAll(true)
      clearSelected()
    }
  };

  const filteredList = useMemo(() => {
    if (!cartridgeList.length) return [];
    const lowerFilterText = filterText.toLowerCase();
    
    return cartridgeList.filter((item) => {
      const id_str = String(item.id)
      const matchesFilter = id_str.toLowerCase().includes(lowerFilterText);
      
      const matchesType = selectedTypes.length === 0 || selectedTypes.includes(Number(item.type));
      const passedQc = item.passed_qc
      return matchesFilter && matchesType && (!showOnlyPassed || passedQc);
    });
  }, [cartridgeList, filterText, selectedTypes, showOnlyPassed]);

  
  
  useEffect(() => {
    if (filteredList.length === 0) {
      setSelectAll(true);
      return;
    }
    const allFilteredSelected = filteredList.every(item => selectedCartridgeList.has(item.id));
    setSelectAll(!allFilteredSelected);
  }, [filteredList, selectedCartridgeList]);


  if (!checkDone || loading) { return <div>Loading Cartridge Data...</div>;}

  if (cartridgeList.length === 0) { return <div>No cartridge data available.</div>;}

  if (filteredList.length === 0) { return <div>No cartridges match your current filters.</div>; }

  return (
    <div>
      <div style={{display: "flex"}}>
      <button style={{
          margin: "0.5em",
          padding: "0.5em"
      }}
              onClick={handleSelectAll}>
        { selectAll ? "select all" : "de-select all" }
      </button>
      </div>
    <div className="list_container">
      {filteredList.map((d) => (
        <CartridgeListItem key={d.id} id={d.id} time={d.b_time} date={d.b_date} type={d.type} status={d.passed_qc}/>
      ))}
    </div>
    </div>
  );
}

export default CartridgeList;
