import './TopContainerDates.css';
import DatePicker from "react-datepicker";
import { DropdownFilter } from "../../components";
import { useFilter } from '../../contexts';

function TopContainerDates() {
  
  const {
    prodStartDate, prodEndDate, setProdStartDate, setProdEndDate,
    qcDateRange, setQCDateRange
  } = useFilter();
  

  const handleProdRangeChange = (dates: [Date | null, Date | null]) => {
    const [start, end] = dates;
    setProdStartDate(start as Date);
    setProdEndDate(end as Date);
  };

  const handleQCRangeChange = (dates: [Date | null, Date | null]) => {
    const [start, end] = dates
    setQCDateRange([start as Date, end as Date]);
  };

  return (
    <div className="topContainer-dates">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <p>
          Production Date:
        </p>
        <DatePicker
          selectsRange
          startDate={prodStartDate}
          endDate={prodEndDate}
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
