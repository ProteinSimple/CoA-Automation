import { CartridgeListItem } from "../../components";
import "./cartridgeList.css";
import { useControl, useCartridge } from "../../contexts";



function CartridgeList() {
  const { checkDone, cartridgeLoading } = useControl();
  const { cartridgeList, filteredList } = useCartridge();


  


  if (!checkDone || cartridgeLoading) { return <div> Loading Cartridge Data...</div>;}

  if (cartridgeList.length === 0) { return <div> No cartridge data available.</div>;}

  if (filteredList.length === 0) { return <div> No cartridges match your current filters.</div>; }

  return (
    <div>
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
