import { useState } from "react";
import "./checkbox.css"

type CheckboxProps = {
  id: string;
  onChecked?: (data: string) => void;
  onUnchecked?: (data: string) => void;
};

function Checkbox ({ id, onChecked, onUnchecked } : CheckboxProps) {
  const [checked, setChecked] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const isChecked = e.target.checked;
    setChecked(isChecked);

    if (isChecked) {
      onChecked?.(id);
    } else {
      onUnchecked?.(id);
    }
  };


  return (
    <label className="checkbox-wrapper"
           id={id}>
    <input type="checkbox"
           checked={checked}
           onChange={handleChange}/>
    <span className="custom-checkbox"></span>
    </label>
  )
}

export default Checkbox;
