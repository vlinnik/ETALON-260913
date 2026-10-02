project init --user vlinnik
devices add --type PYPLC --args device=192.168.1.10 --test PLC
simulator task --name master --exec "src/plc/krax.py" -w src/plc
modules use --test --args panels='doserpanel_.*' concrete6
window add --widget QWidget --name Home home.ui
window add --widget QWidget --name Extensions extensions.ui
window navbar --title 'АСУ БСУ ETALON-260913 (c) ЭТАЛОН-КОМ 2026' --tools Extensions Home 
