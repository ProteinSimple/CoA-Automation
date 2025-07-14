import './DropdownFilter.css';
import { MultiSelect } from 'primereact/multiselect';
import { useEffect, useState } from 'react';
import { useFilter } from '../../contexts';




function DropdownFilter() {
  const [options, setOptions] = useState([
    { label: '1', value: 1 },
    { label: '2', value: 2 },
    { label: '6', value: 6 },
    { label: '8', value: 8 }
  ])
  const [selectedOptions, setSelectedOptions] = useState<number[]>([]);
  const { setTypes, validTypes, colorMap } = useFilter()
  useEffect(() => {
    setTypes(selectedOptions)
  }, [selectedOptions])

  useEffect(() => {
    setOptions(validTypes.map(v => ({ label: String(v), value: v})))
  }, [validTypes]);

  const optionTemplate = (option: { label: string, value: number }) => {
    const color = colorMap?.[option.value] ?? '#ccc';
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span
          style={{
            width: '0.75rem',
            height: '0.75rem',
            borderRadius: '50%',
            backgroundColor: color,
            display: 'inline-block',
          }}
        />
        <span>{option.label}</span>
      </div>
    );
  };

  
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
        optionLabel="label"
        optionValue="value"
        itemTemplate={optionTemplate}
      />
    </div>
  );
}

export default DropdownFilter;