import { usePopUp } from '../../contexts';
import './ErrorPopUpContainer.css';
import Modal from "react-modal"


function ErrorPopUpContainer() {
  const suggestions = [
    "A file the app is trying to write to is currently open in another program.",
    "You are not connected to the internet.",
    "Some of the required files may be missing or corrupted.",
    "The app does not have permission to access the required files or directories.",
    "You have given the program a path that doesn't exists in the settings.",
    "Your antivirus or security software may be blocking the app.",
    "Try restarting the app and ensuring all updates are installed."
  ];
  const { error, setError } = usePopUp()


  return (
    <Modal isOpen={error[0]} className="errorPopUpContainer-container" closeTimeoutMS={300}
        overlayClassName="my-modal-overlay" onRequestClose={() => setError([false, error[1]])}>
      <button onClick={() => setError([false, error[1]])}> X</button>
      <div className='errorPopUpMessage'>
          {error[1]}
      </div>
      <div className='errorPopUpSuggestions'>
        Possible causes of the issue:
        <ul>
          {suggestions.map((s, idx) => <li key={idx}>{s}</li>)}
        </ul>
      </div>
    </Modal>
  );
};

export default ErrorPopUpContainer;
