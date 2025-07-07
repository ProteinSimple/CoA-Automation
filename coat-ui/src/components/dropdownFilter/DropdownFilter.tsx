import './DropdownFilter.css';
import { MultiSelect } from 'primereact/multiselect';
import { useEffect, useState } from 'react';
import { useDate } from '../../contexts';


function DropdownFilter() {
  const [options, setOptions] = useState([
    { label: '1', value: 1 },
    { label: '2', value: 2 },
    { label: '6', value: 6 },
    { label: '8', value: 8 }
  ])
  const [selectedOptions, setSelectedOptions] = useState<number[]>([]);
  const { selectedTypes, setTypes, validTypes } = useDate()
  useEffect(() => {
    setTypes(selectedOptions)
    console.log(selectedTypes)
  }, [selectedOptions])

  useEffect(() => {
    setOptions(validTypes.map(v => ({ label: String(v), value: v})))
    console.log(validTypes)
  }, [validTypes]);


  return (
    <div className="dropdown-container">
      <MultiSelect
        value={selectedOptions}
        options={options}
        onChange={(e) => setSelectedOptions(e.value)}
        placeholder="Cartridge types"
        display="chip"
        className="p-multiselect-dark"
        showSelectAll={false}
      />
    </div>
  );
}

export default DropdownFilter;