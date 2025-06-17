import "./cartridgeListItem.css"
import Checkbox from "../checkbox/Checkbox"

type ListItemProps = {
  id: string;
  time: string;
};

function ListItem( { id, time }: ListItemProps) {
  return (
    <div className="list_item">
      <Checkbox id={id}>
      </Checkbox>
      <p>
        {id}
      </p> 
      <p className="list_item_date">
        {time}
      </p> 
    </div>
    
  )
}

export default ListItem;