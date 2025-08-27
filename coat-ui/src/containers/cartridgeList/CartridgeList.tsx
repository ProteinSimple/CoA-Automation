import { ListItem } from "../../components";
import "./cartridgeList.css";
import { useControl, useCartridge, useFilter } from "../../contexts";



function CartridgeList() {
  const { checkDone, cartridgeLoading } = useControl();
  const { cartridgeList, filteredList, selectedCartridgeList,
          addSelectedCartridge, removeSelectedCartridge 
  } = useCartridge();
  const { showRunTime, showOnlyPassed } = useFilter()

  let content = null;

  if (!checkDone || cartridgeLoading) {
     content = (
      <div className="placeholder">
        Loading Cartridge Data<span className="dots"></span>
      </div>
     );
  } else if (cartridgeList.length === 0) {
    content = <div className="placeholder">No cartridge data available.</div>;
  } else if (filteredList.length === 0) {
    content = <div className="placeholder">No cartridge matches your current filters.</div>;
  } else {
    content = filteredList.map((d) => (
      <ListItem
        topContent={String(d.id)}
        bottomContent={
          showRunTime? d.qc_date + " " + d.qc_time
          : d.qc_analysis_date + " " + d.qc_analysis_time
        }
        isChecked={() => selectedCartridgeList.has(d.id)}
        onChecked={() => addSelectedCartridge(d.id)}
        onUnchecked={() => removeSelectedCartridge(d.id)}
        showMark={!showOnlyPassed}
        key={d.id}
        id={d.id}
        type={d.class_code}
        status={d.qc_status}
        color={d.color}
      />
    ));
  }

  return (
    <div>
      <div className="list_container">
        {content}
      </div>
    </div>
  );
}

export default CartridgeList;
