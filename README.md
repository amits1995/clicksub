# clicksub
quickly right click on a video file to download it's corresponding Hebrew subtitle
# installation
1. make sure you have python 2.7 installed.  
2. install all the required packages from 'requirements.txt'  
3. add a registry key HKEY_CLASSES_ROOT\*\shell\Download Subtitles\command and set Default value: 'python "%script_folder%\main.py" %1'
