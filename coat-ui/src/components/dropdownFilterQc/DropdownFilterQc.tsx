import { useEffect, useState } from 'react';
import { useFilter } from '../../contexts';
import './DropdownFilterQc.css';
import { MultiSelect } from 'primereact/multiselect';


function DropdownFilterQc() {
  const { validUsers, setSelectedUsers } = useFilter()
  const optionTemplate = (option: { label: string, value: number }) => {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span>{option.label}</span>
      </div>
    );
  };

  


  const [options, setOptions] = useState<{ label: string; value: string; }[]>([
    {label: "QC1", value: "1"},
    {label: "QC2", value: "2"},
  ])
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);

  useEffect(() => {
      setOptions(validUsers.map(v => ({ label: String(v), value: v})))
    }, [validUsers]);

  useEffect(() => {
    setSelectedUsers(selectedOptions)
  }, [selectedOptions])
  
  return (
    <div className="dropdown-container">
      <MultiSelect
        value={selectedOptions}
        options={options}
        onChange={(e) => setSelectedOptions(e.value)}
        placeholder="QC user"
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


export default DropdownFilterQc;