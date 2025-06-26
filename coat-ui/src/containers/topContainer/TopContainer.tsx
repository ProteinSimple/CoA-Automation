import "./TopContainer.css";
import { pythonCoa } from "../../services";
import { useCartridge } from "../../contexts";
import { useState } from "react";
import { DotLoader } from "react-spinners";

type ErrorTuple = [boolean, string];

interface TopContainerProps {
  setFilter: (given: string) => void;
  setError: (_: ErrorTuple) => void;
}
function TopContainer({ setFilter, setError }: TopContainerProps) {
  const { selectedCartridgeList } = useCartridge();
  const [ fetchFin, setFetchFin ] = useState(true)

  async function generate() {

    setFetchFin(false)

    try {
      const outputed_files = await pythonCoa([...selectedCartridgeList]);
      if (Array.isArray(outputed_files)) {
        const message = `Following files were created in the process of generation!\n\n${outputed_files.join(
          "\n"
        )}`;
        alert(message);
      } else {
        throw new Error("Unexpected output format from backend.");
      }
    } catch (err: any) {
      const errMsg = err?.message || typeof err == "string"
        ? err.toString()
        : "An uknown error occured during generation!";
      setError([true, errMsg])
    } finally {
      setFetchFin(true)
    }
  }

  return (
    <div className="topContainer-container">
      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          generate();
        }}
      >
        
        <input
          id="SN-search"
          placeholder="Search... 🔍"
          onChange={(e) => setFilter(e.target.value)}
        />
        <input id="greet-input" placeholder="Enter a name..." />
        
        <button type="submit" disabled={!fetchFin}>
          {fetchFin? "Generate" : 
              <DotLoader color="white" loading={!fetchFin} size={20} />}
       </button>
      </form>
    </div>
  );
}

export default TopContainer;
