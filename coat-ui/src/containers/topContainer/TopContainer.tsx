import "./TopContainer.css";
import { pythonCoa } from "../../services";
import  TopContainerFilters  from "../topContainerFilters/TopContainerFilters"
import { useCartridge, useFilter, usePopUp } from "../../contexts";
import { useState } from "react";
import { DotLoader } from "react-spinners";
import "react-datepicker/dist/react-datepicker.css";
import { MyDatePicker } from "../../components";



function TopContainer() {
  
  const { selectedCartridgeList, filteredList } = useCartridge();
  const [ isGenerating, setIsGenerating ] = useState(false)
  const { setError } = usePopUp()
  const [ name, setName ] = useState<string>("")
  const { prodDateRange, setQCDateRange, qcDateRange, setFilterText } = useFilter()
  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (name.length == 0) {
      alert("No name given to sign the mapping file. please provide your name and last name seperated by space")
      return
    }
    setIsGenerating(true);

    try {
      // selectdCartridgeList
      // filteredCartridgeList CartridgeInfo
      const filteredIds = new Set(filteredList.map(c => c.id));
      //
      const targetSet = new Set(
        [...selectedCartridgeList].filter(id => filteredIds.has(id))
      );

      if (targetSet.size === 0) {
        alert("No cartridges are selected for generation!")
        return
      }
        
      const outputed_files = await pythonCoa([...targetSet], name.trim(), prodDateRange[0], prodDateRange[1]);
      let fileList: string[] = [];

      if (typeof outputed_files === "string") {
        fileList = outputed_files.trim().split("\n").filter(Boolean); // Remove empty lines
      } else if (Array.isArray(outputed_files)) {
        fileList = outputed_files;
      } else {
        throw new Error("Unexpected output format from backend.");
      }

      if (fileList.length > 0) {
        let pdf_count = 0; let  csv_count = 0;
        for (const file of fileList) {
          if (file.includes(".pdf")) pdf_count++;
          if (file.includes(".csv")) csv_count++;
        }
        const message = `${pdf_count} CoA files and ${csv_count} mapping file were created.\nFollowing files were created in the process of generation!\n\n${fileList.join("\n")}`;
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
  
  const handleQCRangeChange = (dates: [Date | null, Date | null]) => {
    setQCDateRange([dates[0] as Date, dates[1] as Date]);
  };

  return (
    <div className="topContainer">
      <form
        className="row"
        onSubmit={handleSubmit}>  
        <MyDatePicker 
          headline="QC Run Date"
          dateRange={qcDateRange}
          onChange={handleQCRangeChange}/>
          
        <input className="top-field" id="SN-search"
               placeholder="Search... 🔍"
               onChange={(e) => setFilterText(e.target.value)}/>
        <input className="top-field" id="greet-input"
               placeholder="Enter a name..."
               value={name}
               onChange={(e) => {
                const val = e.target.value;
                  if (/^[a-zA-Z\s]*$/.test(val)) {
                    setName(val);
                  }
                }} />
                      
        <button type="submit"
                disabled={isGenerating}
                style={{display: "flex", alignItems: "center", backgroundColor: "var(--color-button-primary)"}}>
            {isGenerating? (
              <DotLoader color="white" loading={isGenerating} size={20} />
            ) : (
              "Generate"
            )}
        </button>
       </form>
       <TopContainerFilters/>
    </div>
  );
}

export default TopContainer;
