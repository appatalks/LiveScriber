#define AppName "LiveScribe"
#ifndef AppVersion
  #define AppVersion "0.1.0"
#endif

[Setup]
AppId={{A495DCE5-0A02-4D72-9D80-A4A5BC8D8BC5}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=LiveScribe
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir=..\dist\installer
OutputBaseFilename=LiveScribe-Setup-{#AppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=..\assets\livescribe.ico
UninstallDisplayIcon={app}\LiveScribe.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "..\assets\livescribe.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\LiveScribe\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\LiveScribe.exe"; IconFilename: "{app}\livescribe.ico"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\LiveScribe.exe"; IconFilename: "{app}\livescribe.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\LiveScribe.exe"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    DataDir := ExpandConstant('{%USERPROFILE}\.livescribe');
    if DirExists(DataDir) then
    begin
      if MsgBox('Remove all LiveScribe user data?' + #13#10 + #13#10 +
                'This deletes your settings, license key, downloaded models, ' +
                'and recordings stored in:' + #13#10 + DataDir + #13#10 + #13#10 +
                'Choose No to keep your data for a future installation.',
                mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
      begin
        DelTree(DataDir, True, True, True);
      end;
    end;
  end;
end;