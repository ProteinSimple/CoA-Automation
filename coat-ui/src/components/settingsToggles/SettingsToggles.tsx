import { useFilter } from "../../contexts";


function SettingsToggles() {
  const { showOnlyPassed, setShowOnlyPassed, showRunTime, setShowRunTime } = useFilter();
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
          checked={showRunTime}
          onChange={(e) => setShowRunTime(e.target.checked)}
        />
        Show Run time instead of Analysis time
      </label>
    </div>
  )
}

export default SettingsToggles;