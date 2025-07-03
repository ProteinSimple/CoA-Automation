import './SettingPathListItem.css';

interface SettingPathProp {
  path: string,
  deleteAction: (_: string) => void
}

function SettingPathListItem( { path, deleteAction } : SettingPathProp) {
  return (
    <div className="settingPathListItem" key={path}>
      <p>
        {path}
      </p>
      <button onClick={() => deleteAction(path)}>
        delete
      </button>
    </div>
  );
}

export default SettingPathListItem;