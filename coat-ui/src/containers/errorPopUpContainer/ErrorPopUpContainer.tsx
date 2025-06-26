// import { useState } from 'react';
import './ErrorPopUpContainer.css';
import Modal from "react-modal"


type ErrorTuple = [boolean, string];

interface ErrorProps {
  errorTup: ErrorTuple,
  setError: (_: ErrorTuple) => void
}

function ErrorPopUpContainer( { errorTup, setError } : ErrorProps) {
  const suggestions = [
    "A file the app is trying to write to is currently open in another program.",
    "You are not connected to the internet.",
    "Some of the required files may be missing or corrupted.",
    "The app does not have permission to access the required files or directories.",
    "Your antivirus or security software may be blocking the app.",
    "Try restarting the app and ensuring all updates are installed."
];
  return (
    <Modal isOpen={errorTup[0]} className="errorPopUpContainer-container" closeTimeoutMS={300}
        overlayClassName="my-modal-overlay" onRequestClose={() => setError([false, errorTup[1]])}>
      <button onClick={() => setError([false, errorTup[1]])}> X</button>
      <div className='errorPopUpMessage'>
          {errorTup[1]}
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
