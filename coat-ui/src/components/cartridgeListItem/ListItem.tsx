import "./listItem.css"
import Checkbox from "../checkbox/Checkbox"
import { Check, X  } from "lucide-react";

type ListItemProps = {
  id: number;
  type: string;
  status: string;
  color: string;
  isChecked: () => boolean;
  onChecked?: () => void;
  onUnchecked?: () => void;
  topContent?: string;
  bottomContent?: string;
  showMark?: boolean;
};

function StatusIcon({ status }: { status : string }) {
  const PASS = "P"
  const FAIL = "F"
  return   <div>
      {status === PASS ? <Check size="1em"/>
       : status === FAIL ? <X size="1em"/> 
       : <span>?</span> }
    </div>
}

const ColoredDot = ({ color } : { color: string}) => {
  return(
    <span
      data-testid="colored-dot"
        style={{
          width: '0.75rem',
          height: '0.75rem',
          borderRadius: '50%',
          backgroundColor: color ?? '#ccc',
          display: 'inline-block',
          marginRight: '0.5rem',
      }}
    />
  )
}

function ListItem( { topContent, bottomContent, showMark, id, type: label, status, color, isChecked, onChecked, onUnchecked }: ListItemProps) {

  return (
    <div className="list_item">
      <Checkbox  id={id}
                 onChecked={onChecked}
                 onUnchecked={onUnchecked}
                 isChecked={isChecked}>
      </Checkbox>
      <div className="list_item_infobox">
        <p>
          {topContent? topContent : "N/A"}
        </p>
        <p style={{fontSize: "0.8em"}} className="list_item_date">
          { bottomContent? bottomContent : "N/A" }
        </p>  
      {showMark? <StatusIcon status={status}/> : <p></p>}
      </div>
      <p className="list_item_type">
      <ColoredDot color={color}/>
      {label}
      </p>
    </div>
    
  )
}

export default ListItem;