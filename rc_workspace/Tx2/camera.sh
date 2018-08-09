gnome-terminal -x zsh -c "python3 ~/summer-research/rc_workspace/Tx2/collector/controlMaster.py;zsh"
sleep 0.2
gnome-terminal -x zsh -c "python3 ~/summer-research/rc_workspace/Tx2/collector/leftSlave.py;zsh"
sleep 0.2
gnome-terminal -x zsh -c "python3 ~/summer-research/rc_workspace/Tx2/collector/rightSlave.py;zsh"
sleep 0.2
gnome-terminal -x zsh -c "python3 ~/summer-research/rc_workspace/Tx2/collector/centreSlave.py;zsh"

