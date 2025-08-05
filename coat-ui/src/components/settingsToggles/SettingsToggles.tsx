import { useFilter } from "../../contexts";


function SettingsToggles() {
  const { showOnlyPassed, setShowOnlyPassed, showProdTime, setShowProdTime } = useFilter();
  return (
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
  )
}

export default SettingsToggles;