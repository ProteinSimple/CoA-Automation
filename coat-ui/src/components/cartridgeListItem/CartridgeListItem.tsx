import "./cartridgeListItem.css"
import Checkbox from "../checkbox/Checkbox"
import { useCartridge } from "../../contexts";

type ListItemProps = {
  id: string;
  time: string;
};

function ListItem( { id, time}: ListItemProps) {
  const {addCartridge, removeCartridge} = useCartridge()
  return (
    <div className="list_item">
      <Checkbox  id={id}
                 onChecked={addCartridge}
                 onUnchecked={removeCartridge}>
      </Checkbox>
      <div className="list_item_infobox">
        <p>
          {id}
        </p> 
        <p className="list_item_date">
          {time}
        </p> 
      </div>
    </div>
    
  )
}

export default ListItem;