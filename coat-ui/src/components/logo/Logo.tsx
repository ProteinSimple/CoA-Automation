import logo from "../../assets/ProteinSimple-horiz-white.png";
import { Settings } from "lucide-react";
import "./logo.css"
import { usePopUp } from "../../contexts";


function Logo() {
    const { showSettings } = usePopUp()
    return (
        <div className="logo-container">
            <img src={logo} alt="logo-placeholder" className="logo" />
            <button className="settings-btn" style={{"color": "white", marginRight: "0.5em"}}
                    onClick={showSettings}>
                <Settings size={30}/>
            </button>
        </div>
    )
}


export default Logo;