pip3 install pygame
cd $HOME
git clone https://github.com/NathanK4261/DodgeTheAsteroids.git
cd DodgeTheAsteroids
unzip BETA3.5.zip
rm -dPRrvW __MACOSX || echo "Skipping MacOS file cleanup"
rm -f BETA3.5.zip
ls
cd BETA3.5
python3 __buildgame__.py
cd 
cd Desktop
chmod +x DodgeTheAsteroids.command
