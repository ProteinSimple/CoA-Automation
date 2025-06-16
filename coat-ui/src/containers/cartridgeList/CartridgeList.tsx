import { CartridgeListItem } from "../../components";
import "./cartridgeList.css"

interface CatridgeData {
    SN: string;
    time: string;
    man_date: string;
    exp_date: string;
}

interface CartridgeListProps {
  data: CatridgeData[];
}

function CartridgeList({ data } : CartridgeListProps ) {
    return (
        <div className="list_container">
            {data.map(d => <CartridgeListItem id={d.SN} time={d.time} date={d.man_date}/>)}
        </div>
    )
}

export default CartridgeList;