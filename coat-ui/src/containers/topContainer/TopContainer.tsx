import "./TopContainer.css";
import { pythonCoa } from "../../services";
import { useCartridge, useDate, usePopUp } from "../../contexts";
import { useState } from "react";
import { DotLoader } from "react-spinners";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

interface TopContainerProps {
  setFilter: (given: string) => void;
}
function TopContainer({ setFilter }: TopContainerProps) {
  
  const { selectedCartridgeList } = useCartridge();
  const [ isGenerating, setIsGenerating ] = useState(false)
  const { startDate, endDate, setStartDate, setEndDate } = useDate()
  const { setError } = usePopUp()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);

    try {
      const outputed_files = await pythonCoa([...selectedCartridgeList]);
      let fileList: string[] = [];

      if (typeof outputed_files === "string") {
        fileList = outputed_files.trim().split("\n").filter(Boolean); // Remove empty lines
      } else if (Array.isArray(outputed_files)) {
        fileList = outputed_files;
      } else {
        throw new Error("Unexpected output format from backend.");
      }

      if (fileList.length > 0) {
        const message = `Following files were created in the process of generation!\n\n${fileList.join("\n")}`;
        alert(message);
      } else {
        alert("No files were created.");
      }
    } catch (err: any) {
      const errMsg = typeof err == "string" ? err.toString()
                    : err?.message || "An uknown error occured during generation!";
      setError([true, errMsg])
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="topContainer">
      <form
        className="row"
        onSubmit={handleSubmit}>  
        <input className="top-field" id="SN-search"
               placeholder="Search... 🔍"
               onChange={(e) => setFilter(e.target.value)}/>
        <input className="top-field" id="greet-input" placeholder="Enter a name..." />
          
        <button type="submit" disabled={isGenerating}>
            {isGenerating? (
              <DotLoader color="white" loading={isGenerating} size={20} />
             ) : (
              "Generate"
             )}
        </button>
       </form>

       <div className="topContainer-dates">
          <p>
            Start Date:
          </p>
          <DatePicker 
            selected={startDate} 
            onChange={(date) => setStartDate(date as Date)}
            dateFormat="yyyy-MM-dd" 
            customInput={<input readOnly />} 
          />
          <p>
            End Date:
          </p>
          <DatePicker 
            selected={endDate} 
            onChange={(date) => setEndDate(date as Date)}
            dateFormat="yyyy-MM-dd" 
            customInput={<input readOnly />} 
          />
        </div>
    </div>
  );
}

export default TopContainer;
