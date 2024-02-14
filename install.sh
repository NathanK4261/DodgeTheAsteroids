# Unpack files and remove unnecessary files
unzip BETA3.5.zip
rm -dPRrvW __MACOSX || echo "Skipping MacOS file cleanup"
rm -f BETA3.5.zip

# Build the executable script
python3 BETA3.5/__buildgame__.py
mv DodgeTheAsteroids.command ~/Desktop
chmod +x ~/Desktop/DodgeTheAsteroids.command
