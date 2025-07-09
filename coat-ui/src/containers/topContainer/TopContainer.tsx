import "./TopContainer.css";
import { pythonCoa } from "../../services";
import  TopContainerDates  from "../topContainerDates/TopContainerDates"
import { useCartridge, usePopUp } from "../../contexts";
import { useState } from "react";
import { DotLoader } from "react-spinners";
import "react-datepicker/dist/react-datepicker.css";


interface TopContainerProps {
  setFilter: (given: string) => void;
}



function TopContainer({ setFilter }: TopContainerProps) {
  
  const { selectedCartridgeList } = useCartridge();
  const [ isGenerating, setIsGenerating ] = useState(false)
  const { setError } = usePopUp()
  const [ name, setName ] = useState<string>("")
  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);

    try {
      const outputed_files = await pythonCoa([...selectedCartridgeList], name);
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

  return (
    <div className="topContainer">
      <form
        className="row"
        onSubmit={handleSubmit}>  
        <input className="top-field" id="SN-search"
               placeholder="Search... 🔍"
               onChange={(e) => setFilter(e.target.value)}/>
        <input className="top-field" id="greet-input"
               placeholder="Enter a name..."
               onChange={(e) => setName(e.target.value)} />
          
        <button type="submit" disabled={isGenerating || selectedCartridgeList.size == 0}>
            {isGenerating? (
              <DotLoader color="white" loading={isGenerating} size={20} />
             ) : (
              "Generate"
             )}
        </button>
       </form>
       <TopContainerDates/>
    </div>
  );
}

export default TopContainer;
