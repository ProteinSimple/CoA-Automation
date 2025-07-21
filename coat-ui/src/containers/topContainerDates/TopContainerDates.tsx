import './TopContainerDates.css';
import DatePicker from "react-datepicker";
import { DropdownFilter } from "../../components";
import { useFilter } from '../../contexts';

function TopContainerDates() {
  
  const {
    prodDateRange, setProdDateRange,
    qcDateRange, setQCDateRange
  } = useFilter();
  

  const handleProdRangeChange = (dates: [Date | null, Date | null]) => {
    setProdDateRange([dates[0] as Date, dates[1] as Date])
  };

  const handleQCRangeChange = (dates: [Date | null, Date | null]) => {
    setQCDateRange([dates[0] as Date, dates[1] as Date]);
  };

  return (
    <div className="topContainer-dates">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <p>
          Production Date:
        </p>
        <DatePicker
          selectsRange
          startDate={prodDateRange[0]}
          endDate={prodDateRange[1]}
          onChange={handleProdRangeChange}
          dateFormat="yyyy-MM-dd"
          customInput={<input readOnly className='date-input' />}
          wrapperClassName="date-picker-wrapper"
          placeholderText="Select a date range"
        />  
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <p>
            QC Date:
          </p>
          <DatePicker
            selectsRange
            startDate={qcDateRange[0]}
            endDate={qcDateRange[1]}
            onChange={handleQCRangeChange}
            dateFormat="yyyy-MM-dd"
            customInput={<input readOnly className='date-input' />}
            wrapperClassName="date-picker-wrapper"
            placeholderText="Select a date range"
          />
      </div>
      <DropdownFilter/>
    </div>
  );
};

export default TopContainerDates;
