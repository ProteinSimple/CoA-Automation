import { CartridgeListItem } from "../../components";
import "./cartridgeList.css";
import { useControl, useCartridge } from "../../contexts";



function CartridgeList() {
  const { checkDone, cartridgeLoading } = useControl();
  const { cartridgeList, filteredList } = useCartridge();

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
    content = <div className="placeholder">No cartridges match your current filters.</div>;
  } else {
    content = filteredList.map((d) => (
      <CartridgeListItem
        key={d.id}
        id={d.id}
        prod_time={d.build_time}
        prod_date={d.build_date}
        qc_date={d.qc_date}
        qc_time={d.qc_time}
        type={d.class_code}
        status={d.qc_status}
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
