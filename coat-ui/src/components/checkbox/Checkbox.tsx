import "./checkbox.css"

type CheckboxProps = {
  id: string;
  onChecked?: (data: string) => void;
  onUnchecked?: (data: string) => void;
  isChecked: (data: string) => boolean
};

function Checkbox ({ id, onChecked, onUnchecked, isChecked } : CheckboxProps) {

  const handleChange = (_: React.ChangeEvent<HTMLInputElement>) => {
    if (isChecked(id)) {
      onUnchecked?.(id);
    } else {
      onChecked?.(id);
    }
  };


  return (
    <label className="checkbox-wrapper"
           id={id}>
    <input type="checkbox"
           checked={isChecked(id)}
           onChange={handleChange}/>
    <span className="custom-checkbox"></span>
    </label>
  )
}

export default Checkbox;
