#define AppName "InostIOT"
#define AppVersion "1.1"
#define AppPublisher "Ognjen Galic"
#define AppURL "https://github.com/smclt30p/PCS"
#define PyExe "python-3.6.1.exe"

[Setup]
AppId={{3E28F9A8-9940-4066-A149-96663AB24797}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={userappdata}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=build\
OutputBaseFilename=inostiot-setup-{#AppVersion}
SetupIconFile=desktop\icon.ico
UninstallDisplayIcon={app}\desktop\icon.ico
UninstallDisplayName={#AppName} Uninstall
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Components]
Name: "main"; Description: "InostIOT Script files"; Types: full compact custom; Flags: fixed
Name: "python"; Description: "Python 3.6.1/pip 9.0.1 (system wide)"; Types: full custom;

[Files]
Source: "desktop\*.*";Excludes:"*__pycache__*,settings.ini"; DestDir: "{app}\desktop"; Flags: replacesameversion recursesubdirs; Components: main
Source: "start_desktop.bat"; DestDir: "{app}"; Flags: replacesameversion; Components: main
Source: "py\{#PyExe}"; DestDir: "{app}\py\"; Flags: replacesameversion; AfterInstall: InstallPython; Components: python

[Code]
procedure InstallPython;
var
  ResultCode: Integer;
begin
  if not Exec(ExpandConstant('{app}\py\{#PyExe}'), '/quiet InstallAllUsers=1 PrependPath=1', '', SW_SHOWNORMAL,
    ewWaitUntilTerminated, ResultCode)
  then
    MsgBox('Python failed to install! Please install manually from Python.org, selecting "Add to PATH"!', mbError, MB_OK);
end;


[Icons]
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\InostIOT 2017"; Filename: "{app}\start_desktop.bat"; IconFilename: "{app}\desktop\icon.ico"

