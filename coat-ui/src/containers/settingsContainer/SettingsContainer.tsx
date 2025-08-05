import './SettingsContainer.css';
import Modal from "react-modal";
import { usePopUp, useSettings } from '../../contexts';
import SettingsPathList from "../settingsPathList/SettingsPathList";
import { SettingsToggles, CloseButton } from '../../components';


function SettingsContainer() {

  const overlayStyleClass = {
    base: "settings-modal-overlay",
    afterOpen: "ReactModal__Overlay--after-open",
    beforeClose: "ReactModal__Overlay--before-close",      
  }  

  const mainStyleClass = {
    base: "settings-modal-container",
    afterOpen: "ReactModal__Content--after-open",
    beforeClose: "ReactModal__Content--before-close",
  }

  const { setting, hideSettings} = usePopUp()
  const { 
    pdfPaths, addPdfPath, removePdfPath, 
    mappingPaths, addMappingPath, removeMappingPath
  } = useSettings();

  
  return (
    <Modal
      isOpen={setting}
      onRequestClose={hideSettings}
      contentLabel="Settings Modal"
      overlayClassName={overlayStyleClass}
      className={mainStyleClass}
      closeTimeoutMS={300}
      ariaHideApp={false}
    >
      <h4 style={{fontSize: "16px"}}>Settings</h4>
      <div className="settings-content-container">
        <SettingsToggles/>
        <SettingsPathList addPathFunc={addPdfPath} removePathFunc={removePdfPath} paths={pdfPaths} />
        <SettingsPathList addPathFunc={addMappingPath} removePathFunc={removeMappingPath} paths={mappingPaths} />
      </div>
      <CloseButton onClick={hideSettings}></CloseButton>
    </Modal>
  );
};

export default SettingsContainer;
