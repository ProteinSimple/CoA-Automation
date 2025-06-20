import './TopContainer.css';
import { pythonCoa } from '../../services';

interface TopContainerProps {
  selected: string[],
  setFilter: (given: string) => void;
}

function TopContainer({ selected, setFilter } : TopContainerProps) {
  async function greet() {
    await pythonCoa(selected[0])
    console.log(selected)
    
  }

  return (
    <div className="topContainer-container">
      <form className="row"
            onSubmit={(e) => {
              e.preventDefault();
              greet();}}>
        
        <div>
          <input
            id="SN-search"
            placeholder="Search 🔍"
            onChange={(e) => setFilter(e.target.value)}/>
          <input
            id="greet-input"
            placeholder="Enter a name..."/>
        </div>
        <button type="submit"> Generate </button>
      </form>
    </div>
  );
};

export default TopContainer;
