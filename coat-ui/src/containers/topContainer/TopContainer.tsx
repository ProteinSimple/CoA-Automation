import './TopContainer.css';
import { testPythoncom } from '../../services';

function TopContainer() {
  async function greet() {
    let mes = await testPythoncom()
    console.log(mes)
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
            placeholder="Search 🔍"/>
          <input
            id="greet-input"
            placeholder="Enter a name..."/>
        </div>
        <button type="submit">Greet</button>
      </form>
    </div>
  );
};

export default TopContainer;
