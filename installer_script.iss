; Library Management System — Inno Setup installer script
; Compile this with Inno Setup Compiler to produce a full Windows installer.

[Setup]
AppName=Library Management System
AppVersion=1.1.2
AppPublisher=Your Name
DefaultDirName={autopf}\LibraryManagementSystem
DefaultGroupName=Library Management System
OutputDir=installer_output
OutputBaseFilename=LibraryManagementSystem_Setup
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
; Uncomment the line below once you have a .ico file for the app:
; SetupIconFile=app_icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
; This is the single .exe PyInstaller built for you in the dist\ folder.
; library.png is already bundled INSIDE this .exe (via --add-data), so
; it does not need to be listed separately here.
Source: "dist\LibraryManagementSystem.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu entry (appears under "Library Management System" folder)
Name: "{group}\Library Management System"; Filename: "{app}\LibraryManagementSystem.exe"
; Start Menu uninstall entry
Name: "{group}\Uninstall Library Management System"; Filename: "{uninstallexe}"
; Optional desktop shortcut (only created if the user checks the box during install)
Name: "{autodesktop}\Library Management System"; Filename: "{app}\LibraryManagementSystem.exe"; Tasks: desktopicon

[Run]
; Offers to launch the app right after installation finishes
Filename: "{app}\LibraryManagementSystem.exe"; Description: "Launch Library Management System"; Flags: nowait postinstall skipifsilent