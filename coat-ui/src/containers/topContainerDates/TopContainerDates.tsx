import './TopContainerDates.css';
import DatePicker from "react-datepicker";
import { DropdownFilter } from "../../components";
import { useFilter } from '../../contexts';

function TopContainerDates() {
  
  const { startDate, endDate, setStartDate, setEndDate } = useFilter()

  return (
    <div className="topContainer-dates">
          <p>
            Start Date:
          </p>
          <DatePicker 
            selected={startDate} 
            onChange={(date) => setStartDate(date as Date)}
            dateFormat="yyyy-MM-dd" 
            customInput={<input readOnly  className='date-input'/>}
            wrapperClassName="date-picker-wrapper" 
          />
          <p>
            End Date:
          </p>
          <DatePicker 
            selected={endDate} 
            onChange={(date) => setEndDate(date as Date)}
            dateFormat="yyyy-MM-dd" 
            customInput={<input readOnly className='date-input'/>} 
            wrapperClassName="date-picker-wrapper"
          />
          <DropdownFilter/>
    </div>
  );
};

export default TopContainerDates;
