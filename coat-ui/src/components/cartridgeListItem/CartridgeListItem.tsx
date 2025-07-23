import "./cartridgeListItem.css"
import Checkbox from "../checkbox/Checkbox"
import { useCartridge } from "../../contexts";
import { useFilter } from "../../contexts";
import { Check, X  } from "lucide-react";

type ListItemProps = {
  id: number;
  prod_date: string;
  prod_time: string;
  qc_date: string;
  qc_time: string;
  type: string;
  status: string
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

function ListItem( { id, prod_date, prod_time, qc_date, qc_time, type, status }: ListItemProps) {
  const { selectedCartridgeList, addSelectedCartridge: addCartridge, removeSelectedCartridge: removeCartridge } = useCartridge()
  const isChecked = () => { return selectedCartridgeList.has(id) }
  const onChecked = () => { addCartridge(id) }
  const onUnchecked = () => { removeCartridge(id) }
  const { colorMap, showOnlyPassed, showProdTime } = useFilter()
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
        {showProdTime?
          <p style={{fontSize: "0.8em"}} className="list_item_date">
            {prod_date} {prod_time}
          </p>
          : qc_date && qc_time ? 
          <p style={{fontSize: "0.8em"}} className="list_item_date">
            {qc_date} {qc_time} 
          </p>
          :
          <p className="list_item_date">
            NA 
          </p>
        } 
        
          {!showOnlyPassed ? <StatusIcon status={status}/> : <p></p>}
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