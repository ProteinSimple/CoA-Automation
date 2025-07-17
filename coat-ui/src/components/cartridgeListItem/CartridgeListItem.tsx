import "./cartridgeListItem.css"
import Checkbox from "../checkbox/Checkbox"
import { useCartridge } from "../../contexts";
import { useFilter } from "../../contexts";
import { Check, X } from "lucide-react";

type ListItemProps = {
  id: number;
  time: string;
  type: string;
  passed: boolean
};

function ListItem( { id, time, type, passed }: ListItemProps) {
  const { selectedCartridgeList, addCartridge, removeCartridge } = useCartridge()
  const isChecked = () => { return selectedCartridgeList.has(id) }
  const onChecked = () => { addCartridge(id) }
  const onUnchecked = () => { removeCartridge(id) }
  const { colorMap, showOnlyPassed } = useFilter()
  return (
    <div className="list_item">
      <Checkbox  id={id}
                 onChecked={onChecked}
                 onUnchecked={onUnchecked}
                 isChecked={isChecked}>
      </Checkbox>
      <div className="list_item_infobox">
        <p>
          {id}
        </p> 
        <p className="list_item_date">
          {time}
        </p>
          {!showOnlyPassed && passed? <Check size="1em"/> : !showOnlyPassed && !passed? <X size="1em"/> : <p></p>}
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