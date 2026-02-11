# 🎮 Stellar Blade SteamID Editor

![GitHub release](https://img.shields.io/github/v/release/mendeseskel/StellarBlade-SteamID-Editor)
![License](https://img.shields.io/github/license/mendeseskel/StellarBlade-SteamID-Editor)

A tool to transfer Stellar Blade save games between different Steam accounts by modifying the SteamID in save files and renaming save folders.

## 📥 Download
Get the latest release from the [Releases page](https://github.com/mendeseskel/StellarBlade-SteamID-Editor/releases).

## 🚀 Features
- ✅ Load SteamID from configs.user.ini automatically
- ✅ Replace SteamID in .sav files
- ✅ Rename save folder to match new SteamID
- ✅ Automatic backup (.bak) creation
- ✅ 17-digit SteamID validation
- ✅ Clean and intuitive interface

## 🛠️ How to Use
### 1. Find your files:
```
Save: AppData\Local\SB\Saved\SaveGames\FOLDER-WITH-NUMBERS\
Config: steam_settings\configs.user.ini
```

### 2. Copy your new SteamID:
Open `configs.user.ini` and copy:
```ini
account_steamid=7656119xxxxxxxxxx
```

### 3. Use the program:
1. Run `SB SteamID Editor.exe`
2. Click "Load Config File" → select `configs.user.ini`
3. Click "Browse" → select `StellarBladeSave00.sav`
4. Click "Replace SteamID & Rename Folder"
5. Done!
```

## ⚠️ Important Notes
- Always backup your saves before modifying
- SteamID must be exactly 17 digits
- The save folder name MUST match the SteamID
- Use at your own risk
