import { useState } from 'react';
import './SelectAllButton.css';
import { useCartridge } from '../../contexts';


function SelectAllButton() {

  const [selectAll, setSelectAll] = useState<boolean>(true);
  const { addSelectedCartridge, clearSelected, filteredList } = useCartridge();

  
  const handleSelectAll = () => {
    if(selectAll) {
      setSelectAll(false)
      filteredList.map(v => addSelectedCartridge(v.id))
    } else {
      setSelectAll(true)
      clearSelected()
    }
  };
  return <div style={{display: "flex"}}>
    <button style={{ margin: "0.5em", padding: "0.5em"}}
            onClick={handleSelectAll}>
    { selectAll ? "select all" : "de-select all" }
    </button>
  </div>
}

export default SelectAllButton;