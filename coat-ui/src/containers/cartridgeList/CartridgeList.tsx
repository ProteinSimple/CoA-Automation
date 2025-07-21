import { CartridgeListItem } from "../../components";
import { pythonFetchRange } from "../../services";
import { useEffect, useState, useMemo, useCallback } from "react";
import "./cartridgeList.css";
import { useCartridge, useControl, useFilter } from "../../contexts";

interface CartridgeInfo {
  id: number;
  build_date: string;
  build_time: string;
  class_code: string;
  qc_status: string;
  qc_date: string;
  qc_time: string
}

interface CartridgeListProps {
  filterText: string
}

function CartridgeList({ filterText }: CartridgeListProps) {
  const [cartridgeList, setCartridgeList] = useState<CartridgeInfo[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const { addCartridge, clearSelected, selectedCartridgeList } = useCartridge()
  const { checkDone } = useControl();
  const {
    prodStartDate, prodEndDate, selectedTypes,
    setValidTypes, showOnlyPassed, qcDateRange 
  } = useFilter()
  const [selectAll, setSelectAll] = useState<boolean>(true)

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const raw = await pythonFetchRange(prodStartDate, prodEndDate);
      const parsed: CartridgeInfo[] = JSON.parse(String(raw));
      const uniqueTypes = [...new Set(parsed.map(item => Number(item.class_code)))];
      setValidTypes(uniqueTypes);
      setCartridgeList([]);
      setCartridgeList(parsed);
    } catch (error) {
      console.error("Error fetching/parsing cartridge list:", error);
      setCartridgeList([]); // Reset on error
    } finally {
      setLoading(false);
    }
  }, [prodStartDate, prodEndDate, setValidTypes]);


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
      
      const matchesType = selectedTypes.length === 0 || selectedTypes.includes(Number(item.class_code));
      const passedQc = item.qc_status === "P"

      const qcDate = new Date(item.qc_date);
      console.log("QC Date:", item.qc_date)
      const [qcStart, qcEnd] = qcDateRange
      const matchesQCDate = qcDate >= qcStart && qcDate <= qcEnd || item.qc_date == null;

      return matchesFilter && matchesQCDate && matchesType && (!showOnlyPassed || passedQc);
    });
  }, [cartridgeList, filterText, selectedTypes, showOnlyPassed, qcDateRange]);

  
  
  useEffect(() => {
    if (filteredList.length === 0) {
      setSelectAll(true);
      return;
    }
    const allFilteredSelected = filteredList.every(item => selectedCartridgeList.has(item.id));
    setSelectAll(!allFilteredSelected);
  }, [filteredList, selectedCartridgeList]);


  if (!checkDone || loading) { return <div> Loading Cartridge Data...</div>;}

  if (cartridgeList.length === 0) { return <div> No cartridge data available.</div>;}

  if (filteredList.length === 0) { return <div> No cartridges match your current filters.</div>; }

  return (
    <div>
      <div style={{display: "flex"}}>
        <button style={{ margin: "0.5em", padding: "0.5em"}}
                onClick={handleSelectAll}>
        { selectAll ? "select all" : "de-select all" }
        </button>
      </div>
      <div className="list_container">
        {filteredList.map(d =>
          <CartridgeListItem
           key={d.id} id={d.id}
           prod_time={d.build_time}
           prod_date={d.build_date}
           qc_date={d.qc_date}
           qc_time={d.qc_time}
           type={d.class_code}
           status={d.qc_status}/>
        )}
      </div>
    </div>
  );
}

export default CartridgeList;
