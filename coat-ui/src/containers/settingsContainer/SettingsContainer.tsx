import './SettingsContainer.css';
import Modal from "react-modal";
import { SettingPathListItem } from '../../components';
import { useState } from 'react';
import { open } from '@tauri-apps/plugin-dialog';

interface Props {
  isOpen: boolean;
  onClose: () => void
}



function SettingsContainer( {isOpen, onClose} : Props) {

  const [paths, setPaths] = useState<string[]>([
    "./out",
    "./out2"
  ])

  const addPath = (given: string) => {
    setPaths(prev => [...prev, given])
  }

  const removePath = (given: string) => {
    setPaths(prev => prev.filter(p => p !== given))
  }

  const handleAddButton = () => {
    const prompted = prompt("Paste your output path here")
    if (prompted != null) { addPath(prompted) }
  }

  const handleFolderButton = async () => {
    const file = await open({
      multiple: false,
      directory: true,
    });
    if (file != null) { addPath(file) }
  }

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      contentLabel="Settings Modal"
      overlayClassName={{
        base: "settings-modal-overlay",
        afterOpen: "ReactModal__Overlay--after-open",
        beforeClose: "ReactModal__Overlay--before-close",
      }}
      className={{
        base: "settings-modal-container",
        afterOpen: "ReactModal__Content--after-open",
        beforeClose: "ReactModal__Content--before-close",
      }}
      closeTimeoutMS={300}
      ariaHideApp={false}
    >
      
      
      <h2>Settings</h2>
      <div>
          <button onClick={handleAddButton}>
            Add button
          </button>
          <button onClick={handleFolderButton}>
            Folder button
          </button>
      </div>
      <div className="settings-modal-message">
        {paths.map((val) => <SettingPathListItem path={val} deleteAction={removePath}/>)}
      </div>
      <button className='setting_x' onClick={onClose}>X</button>
    </Modal>

  );
};

export default SettingsContainer;
