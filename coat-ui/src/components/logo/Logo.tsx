import logo from "../../assets/ProteinSimple-horiz-white.png";
import { Settings } from "lucide-react";
import "./logo.css"

interface LogoProps {
    CogAction: () => void;
};

function Logo({ CogAction }: LogoProps) {

    return (
        <div className="logo-container">
            <img src={logo} alt="logo-placeholder" className="logo" />
            <button className="settings-btn"
                    onClick={CogAction}>
                <Settings size={30}/>
            </button>
        </div>
    )
}


export default Logo;