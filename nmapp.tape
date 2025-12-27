Output nmapp.gif

Require echo

Set Shell "bash"
Set FontSize 24
Set Width 1200
Set Height 600
Set Theme "iTerm2 Dark Background"

Type "nmap -F scanme.nmap.org 8.8.8.8 1.1.1.1 -oX - | nmapp" Sleep 500ms Enter Sleep 500ms Enter Sleep 2000ms

Sleep 5s
