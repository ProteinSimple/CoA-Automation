import DatePicker from 'react-datepicker';
import './MyDatePicker.css';

interface MyDatePickerProps {
  headline: string;
  dateRange: [Date, Date];
  onChange: (_: [Date | null, Date | null]) => void
}

function MyDatePicker( { headline, dateRange, onChange} : MyDatePickerProps) {
  
  return <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <p>
          {headline}
        </p>
        <DatePicker
          selectsRange
          startDate={dateRange[0]}
          endDate={dateRange[1]}
          onChange={onChange}
          dateFormat="yyyy-MM-dd"
          customInput={<input readOnly className='date-input' />}
          wrapperClassName="date-picker-wrapper"
          placeholderText="Select a date range"
        />  
      </div>
}

export default MyDatePicker;