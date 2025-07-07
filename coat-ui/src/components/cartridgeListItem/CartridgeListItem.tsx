import "./cartridgeListItem.css"
import Checkbox from "../checkbox/Checkbox"
import { useCartridge } from "../../contexts";
import { useFilter } from "../../contexts";

type ListItemProps = {
  id: string;
  time: string;
  type: string;
};

function ListItem( { id, time, type }: ListItemProps) {
  const { selectedCartridgeList, addCartridge, removeCartridge } = useCartridge()
  const isChecked = (id: string) => { return selectedCartridgeList.has(id) }
  const [datePart, timePart] = time.split(" ");
  const { colorMap } = useFilter()
  return (
    <div className="list_item">
      <Checkbox  id={id}
                 onChecked={addCartridge}
                 onUnchecked={removeCartridge}
                 isChecked={isChecked}>
      </Checkbox>
      <div className="list_item_infobox">
        <p>
          {id}
        </p> 
        <p className="list_item_date">
          {datePart}
        </p>
        <p className="list_item_date">
          {timePart}
        </p>
      </div>
      <p className="list_item_type">
      <span
        style={{
          width: '0.75rem',
          height: '0.75rem',
          borderRadius: '50%',
          backgroundColor: colorMap?.[parseInt(type)] ?? '#ccc',
          display: 'inline-block',
          marginRight: '0.5rem',
        }}
      />
      {type}
    </p>
    </div>
    
  )
}

export default ListItem;