import { useState } from 'react';
import './SettingPathListItem.css';
import { Trash2 } from 'lucide-react';

interface SettingPathProp {
  path: string,
  deleteAction: (_: string) => void
}

function SettingPathListItem( { path, deleteAction } : SettingPathProp) {
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await deleteAction(path);
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };
  return (
    <div
      id={"<setting>" + path}
      className={`settingPathListItem ${deleting ? 'deleting' : ''}`}
      key={path}
    >
      <div className="path-container">
        <p>{path}</p>
      </div>
      <button onClick={handleDelete} disabled={deleting}>
        <Trash2 size="1em" />
      </button>
    </div>
  );
}

export default SettingPathListItem;