;Include Modern UI
!include "MUI2.nsh"


;General
Name "admineasy"
OutFile "admineasy.exe"

InstallDir "$PROGRAMFILES\admineasy\harvester"
InstallDirRegKey HKCU "Software\admineasy" ""

RequestExecutionLevel admin

;Interface Settings
!define MUI_ABORTWARNING


;Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES


;Languages
!insertmacro MUI_LANGUAGE "French"


;Installer Section
Section "Harvester" harvester

    SetOutPath "$INSTDIR"

    File /r dist\*

    Exec $PROGRAMFILES\admineasy\harvester\harvester-setup\harvester-setup.exe

    ;Store installation folder
    WriteRegStr HKCU "Software\admineasy" "" $INSTDIR

    ;Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd


;Uninstaller Section

Section "Uninstall"

    Exec $PROGRAMFILES\admineasy\harvester\harvester-uninstaller\harvester-uninstaller.exe

    Delete "$INSTDIR\*.*"
    Delete "$INSTDIR\Uninstall.exe"
    Delete "C:\logs\harvester-log.log"

    DeleteRegKey /ifempty HKCU "Software\admineasy"

    RMDir /r "$INSTDIR"

SectionEnd
