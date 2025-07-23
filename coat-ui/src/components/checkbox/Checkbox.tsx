import "./checkbox.css"

type CheckboxProps = {
  id: string | number;
  onChecked?: () => void;
  onUnchecked?: () => void;
  isChecked: () => boolean
};

function Checkbox ({ id, onChecked, onUnchecked, isChecked } : CheckboxProps) {

  const handleChange = (_: React.ChangeEvent<HTMLInputElement>) => {
    if (isChecked()) {
      onUnchecked?.();
    } else {
      onChecked?.();
    }
  };


  return (
    <label className="checkbox-wrapper"
           id={String(id)}>
    <input type="checkbox"
           checked={isChecked()}
           onChange={handleChange}/>
    <span className="custom-checkbox"></span>
    </label>
  )
}

export default Checkbox;
