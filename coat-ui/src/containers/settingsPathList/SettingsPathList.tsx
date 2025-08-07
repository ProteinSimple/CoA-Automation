
import { SettingPathListItem } from '../../components';
import { open  } from '@tauri-apps/plugin-dialog';
import { Folder } from 'lucide-react';



interface SettingPathListProps {
  addPathFunc: (_: string) => void;
  removePathFunc: (_: string) => void;
  paths: string[];
  title?: string;
}

function SettingsPathList({ addPathFunc, removePathFunc, paths, title } : SettingPathListProps) {
  
  const handleAddButton = async () => {
    const prompted = prompt("Paste your output path here")
    if (prompted != null) { 
      addPathFunc(prompted)
    }
  }

  const handleFolderButton = async () => {
    const file = await open({
      multiple: false,
      directory: true,
    });
    if (file != null) { addPathFunc(file) }
  }

  return (
    <div className="settings-path-container">
      {title ? title : "Title"}
      <div>
          <button onClick={handleAddButton}>
            Add path manually
          </button>
          <button onClick={handleFolderButton}>
            <Folder size="1em"/>
          </button>
      </div>
      <div className="settings-modal-message">
        {paths.map((val) => <SettingPathListItem key={val} path={val} deleteAction={removePathFunc}/>)}
      </div>
    </div>
  )
}

export default SettingsPathList;