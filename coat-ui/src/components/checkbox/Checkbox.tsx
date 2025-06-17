import "./checkbox.css"

type CheckboxProps = {
  id: string;
}

function Checkbox ({ id } : CheckboxProps) {
  return (
    <label className="checkbox-wrapper"
           id={id}>
    <input type="checkbox" />
    <span className="custom-checkbox"></span>
    </label>
  )
}

export default Checkbox;
