import './SettingPathListItem.css';
import { Trash2 } from 'lucide-react';

interface SettingPathProp {
  path: string,
  deleteAction: (_: string) => void
}

function SettingPathListItem( { path, deleteAction } : SettingPathProp) {
  return (
    <div id={"<setting>" + path} className="settingPathListItem" key={path}>
      <p>
        {path}
      </p>
      <button onClick={() => deleteAction(path)}>
        <Trash2 size="1em"/>
      </button>
    </div>
  );
}

export default SettingPathListItem;