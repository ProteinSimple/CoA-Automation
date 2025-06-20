import "./cartridgeListItem.css"
import Checkbox from "../checkbox/Checkbox"

type ListItemProps = {
  id: string;
  time: string;
  add: (newCartridge: string) => void;
  remove: (newCartridge: string) => void;
};

function ListItem( { id, time, add, remove }: ListItemProps) {
  return (
    <div className="list_item">
      <Checkbox  id={id}
                 onChecked={add}
                 onUnchecked={remove}>
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