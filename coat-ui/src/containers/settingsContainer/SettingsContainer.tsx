import './SettingsContainer.css';
import Modal from "react-modal";
import { SettingPathListItem } from '../../components';
import { useEffect, useState } from 'react';
import { open  } from '@tauri-apps/plugin-dialog';
import { pythonConfigAddPdf, pythonConfigList, pythonConfigDeletePdf, pythonConfigAddMapping, pythonConfigDeleteMapping } from '../../services';
import { useControl, useFilter, usePopUp } from '../../contexts';
import { Folder } from 'lucide-react';





function SettingsContainer() {

  const [pdfPaths, setPdfPaths] = useState<string[]>([])
  const [mappingPaths, setMappingPaths] = useState<string[]>([])
  const { setting: isOpen, hideSettings: onClose} = usePopUp()
  const { checkDone } = useControl();
  const { showOnlyPassed, setShowOnlyPassed, showProdTime, setShowProdTime } = useFilter();

  const addPdfPath = async (given: string) => {
    try {
        const res = await pythonConfigAddPdf([given])
        const config = JSON.parse(res as string) as { [key: string]: any }
        setPdfPaths(config["pdf_output_dir"])
    } catch (err) {
        console.error("Failed to fetch or parse config:", err);
    }
  }

  

  const removePdfPath = async (given: string) => {
    try {
        const res = await pythonConfigDeletePdf([given])
        const config = JSON.parse(res as string) as { [key: string]: any }
        setPdfPaths(config["pdf_output_dir"])
    } catch (err) {
        console.error("Failed to fetch or parse config:", err);
    }
  }

  const addMappingPath = async (given: string) => {
    try {
        const res = await pythonConfigAddMapping([given])
        const config = JSON.parse(res as string) as { [key: string]: any }
        setMappingPaths(config["mapping_output_dir"])
    } catch (err) {
        console.error("Failed to fetch or parse config:", err);
    }
  }

  const removeMappingPath = async (given: string) => {
    try {
        const res = await pythonConfigDeleteMapping([given])
        const config = JSON.parse(res as string) as { [key: string]: any }
        setMappingPaths(config["mapping_output_dir"])
    } catch (err) {
        console.error("Failed to fetch or parse config:", err);
    }
  }

  const handleAddButton = async (addFunc: (_: string) => void) => {
    const prompted = prompt("Paste your output path here")
    
    if (prompted != null) { 
      addFunc(prompted)
    }
  }

  const handleFolderButton = async (addFunc: (_: string) => void) => {
    const file = await open({
      multiple: false,
      directory: true,
    });
    if (file != null) { addFunc(file) }
  }

  useEffect(() => {
    const effect = async () => {
      if (!checkDone) return
      try {
        const res = await pythonConfigList();
        const config = JSON.parse(res as string) as { [key: string]: any };
        setPdfPaths(config["pdf_output_dir"]);
        setMappingPaths(config["mapping_output_dir"]);
      } catch (err) {
        console.error("Failed to fetch or parse config:", err);
      }
    }
    effect()
  }, [isOpen, checkDone])

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
      <h4 style={{fontSize: "16px"}}>Settings</h4>
      <div className="settings-content-container">
        <div className="settings-toggle-container"
              style={{ display: "flex", flexDirection: "column", justifyContent: "flex-start",
                       paddingTop: "2em", gap: "2em", alignItems: "flex-start"}}>
          <label>
            <input
              type="checkbox"
              checked={showOnlyPassed}
              onChange={(e) => setShowOnlyPassed(e.target.checked)}
            />
            Show only cartridges that passed QC
          </label>
          <label>
            <input
              type="checkbox"
              checked={showProdTime}
              onChange={(e) => setShowProdTime(e.target.checked)}
            />
            Show Production time instead of QC time
          </label>
        </div>
        <div className="settings-path-container">
          COA Output paths
          <div>
              <button onClick={() => handleAddButton(addPdfPath)}>
                Add path manually
              </button>
              <button onClick={() => handleFolderButton(addPdfPath)}>
                <Folder size="1em"/>
              </button>
          </div>
          <div className="settings-modal-message">
            {pdfPaths.map((val) => <SettingPathListItem path={val} deleteAction={removePdfPath}/>)}
          </div>
        </div>
        <div className="settings-path-container">
          Mapping Output paths
          <div>
              <button onClick={() => handleAddButton(addMappingPath)}>
                Add path manually
              </button>
              <button onClick={() => handleFolderButton(addMappingPath)}>
                <Folder size="1em"/>
              </button>
          </div>
          <div className="settings-modal-message">
            {mappingPaths.map((val) => <SettingPathListItem path={val} deleteAction={removeMappingPath}/>)}
          </div>
        </div>
      </div>
      <button className='setting_x' onClick={onClose}>X</button>
    </Modal>

  );
};

export default SettingsContainer;
