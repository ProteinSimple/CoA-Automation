import "./TopContainer.css";
import { pythonCoa } from "../../services";
import { useCartridge } from "../../contexts";
import { useState } from "react";
import { DotLoader } from "react-spinners";


interface TopContainerProps {
  setFilter: (given: string) => void;
}

function TopContainer({ setFilter }: TopContainerProps) {
  const { cartridgeList } = useCartridge();
  const [ fetchFin, setFetchFin ] = useState(true)

  async function generate() {
    setFetchFin(false)
    const outputed_files = await pythonCoa(cartridgeList);
    if (Array.isArray(outputed_files)) {
      const message = `Following files were created in the process of generation!\n\n${outputed_files.join(
        "\n"
      )}`;
      alert(message);
    } else {
      // fallback, but normally shouldn't hit here
      alert("Unexpected output format");
    }
    setFetchFin(true)
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
