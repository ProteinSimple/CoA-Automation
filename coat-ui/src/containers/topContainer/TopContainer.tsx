import "./TopContainer.css";
import { pythonCoa } from "../../services";
import { useCartridge } from "../../contexts";

interface TopContainerProps {
  setFilter: (given: string) => void;
}

function TopContainer({ setFilter }: TopContainerProps) {
  const { cartridgeList } = useCartridge();

  async function generate() {
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
        <div>
          <input
            id="SN-search"
            placeholder="Search... 🔍"
            onChange={(e) => setFilter(e.target.value)}
          />
          <input id="greet-input" placeholder="Enter a name..." />
        </div>
        <button type="submit">Generate</button>
      </form>
    </div>
  );
}

export default TopContainer;
