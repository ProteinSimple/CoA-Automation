import './TopContainerFilters.css';
import { DropdownFilter, DropdownFilterQc, SelectAllButton, MyDatePicker } from "../../components";
import { useFilter } from '../../contexts';


function TopContainerFilters() {
  
  const {
    analysisDateRange: prodDateRange, setAnalysisDateRange: setProdDateRange,
  } = useFilter();
  

  const handleProdRangeChange = (dates: [Date | null, Date | null]) => {
    setProdDateRange([dates[0] as Date, dates[1] as Date])
  };

  return (
    <div className="topContainer-dates">
      <MyDatePicker headline="QC Analysis Date"
                    dateRange={prodDateRange}
                    onChange={handleProdRangeChange} >
      </MyDatePicker>
      <DropdownFilter/>
      <DropdownFilterQc/>
      <SelectAllButton/>
    </div>
  );
};

export default TopContainerFilters;
