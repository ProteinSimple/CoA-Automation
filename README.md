# COAT: Certificate of Analysis Automation Tool
COAT is an internally developed tool by the Operations team to streamline the process of CoA creation and uploading. If you are a user, please look at the [User Guide (coming soon)]() for further instructions. There are simple instructions listed below to use the released version of the product. There are more detailed explanations at the [bottom of the page](#developers-guide). A developer document will be released in the near future.


## Table of Contents

- [1.0 Automation script](#10-release-builds)
- [2.0 Installing the Desktop GUI](#20-installing-the-desktop-gui)
- [3.0 Developer's Guide](#30-developers-guide)

## 1.0 Release builds
All of the approved versions can be found [here](https://github.com/ProteinSimple/CoA-Automation/releases). Make sure you are always using the most recent stable build. Each package comes with an installer for the UI alongside a zipped file containing a PyInstaller "compiled"[*](#pyinstaller-compiled) version of the automation script. If you are a normal user you can just use the installer to run the program. (The User Guide is currently in development).

## 2.0 Developer's Guide
There are two main components to this project. The automation script and the UI.


### 2.1 Automation script
This is written purely in Python, using multiple packages which are listed in the next section. The full script can be found in `./automation/src/`. To run the project, use the following commands in PowerShell. (Linux instructions may be added later.). to install and update Python and the needed packages.
```powershell
winget install Python.Python.3.11
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r pyREQ.txt
```
Then run the following to see a guide for using the `main.py` file:
```bash
python main.py --help
```

### 2.2 UI
The UI is written using Tauri and React. This makes the program very lightweight since it doesn't package chromium inside of the application (unlike Electron.js). You’ll need a PyInstaller build of the automation script. You can generate it using `./bin/buildPy.ps1`

Now let's try running the UI. First, you'll need to install Tauri's requirements:
- [MS C++ build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (desktop development with C++ option only)
- [Web2View](https://developer.microsoft.com/en-us/microsoft-edge/webview2/?form=MA13LH#download-section)
- [Rust](https://www.rust-lang.org/tools/install)
- [Node.js](https://nodejs.org/en/download)

After all of these are installed correctly we can run the UI in development mode:
```bash
cd ./coat-ui/
npm install
npm run tauri dev
```

To get an executable/bundled version of the project :
```
npm run tauri build
```
You can find the bundled version of the program in `./coat-ui/src-tauri/target`.

## 3.0 Technologies Used
- https://tauri.app/
- https://react.dev/
- https://vite.dev/
- https://www.python.org/
- https://pymupdf.readthedocs.io/en/latest/
- https://pypdf.readthedocs.io/en/stable/


## 4.0 Footnotes
#### *Pyinstaller compiled: Technically, Python is not compiled but interpreted. PyInstaller bundles all the required Python packages along with a minimal Python interpreter into a standalone executable, allowing the script to run without needing Python installed