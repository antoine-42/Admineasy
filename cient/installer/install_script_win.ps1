.\nssm.exe install harvester 'C:\Program Files (x86)\admineasy\harvester\harvester\harvester.exe'
.\nssm.exe set harvester Description "Admineasy client."
.\nssm.exe set harvester Start SERVICE_AUTO_START
.\nssm.exe set harvester AppStdout "C:\logs\harvester-log.log"
.\nssm.exe start harvester
