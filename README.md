# Broke Pass

A modern, lightweight, and fully offline password manager built with Python and PyQt5.
Broke Pass focuses on simplicity, customization, and local-first security while providing a clean desktop experience for managing encrypted passwords.

---

# Features

## 🔐 Secure Password Storage

* Stores passwords inside encrypted `.bpass` files
* Uses a custom character-based encryption system
* Supports master password protection
* Fully offline — no cloud syncing or online account required

## 👤 Multi-User Support

* Create multiple password vaults
* Open different `.bpass` files anytime
* Custom usernames and master passwords for each vault

## ⭐ Favorites System

* Mark important passwords as favorites
* Favorites appear at the top of the password list
* Quick access to frequently used accounts

## 🔍 Smart Search

* Search by website name
* Optional password-content searching
* Instant filtering system

## 🎨 Customizable Interface

* Dark mode and light mode
* Multi-language support
* Custom UI styling through JSON stylesheets
* Dynamic font loading using Nunito

## 🧰 Password Tools

* Built-in strong password generator
* One-click clipboard copy
* Show/hide password visibility
* Edit and delete existing entries

## 💾 Import & Export

* Export decrypted backups into `.brokepass` files
* Import backups with automatic config restoration
* File-location management system

## 🔄 Update System

* GitHub-based update checker
* Release notes integration
* OTA updater support through `brokeupdater.exe`

## 🖼️ Modern PyQt5 UI

* Sidebar navigation system
* Scrollable sections
* Image slideshows
* Dialog-based editing
* Responsive layouts and polished styling

---

# Technologies Used

* Python
* PyQt5
* JSON
* Requests
* Pyperclip

---

# Project Structure

```text
assets/
├── config.json
├── lang.json
├── style.json
├── updates.json
├── photos/
├── icons/
├── fonts/
├── exports/
└── default.bpass
```

---

# Main Components

| Component      | Description                                   |
| -------------- | --------------------------------------------- |
| `UI`           | Main application interface                    |
| `Encryption`   | Handles encryption, decryption, import/export |
| `Pwd`          | Individual password entry widget              |
| `SettingCombo` | Dynamic settings dropdown component           |
| `Button`       | Sidebar navigation buttons                    |
| `Slideshow`    | Image slideshow system                        |

---

# Security Notes

* Passwords are stored locally only
* No analytics or telemetry
* No internet connection required for normal operation
* Exported backups are decrypted and should be stored securely
* Custom encryption is used for obfuscation and local protection

---

# Screens Included

The application includes:

* Home page slideshow
* Password manager dashboard
* Settings panel
* Update checker
* Login screen
* About page

---

# Developer

**@br0ke.tech**

* TikTok: `tiktok.com/@br0ke.tech`
* GitHub: `github.com/broke-tech`

---

# License

This project is intended for educational and personal use.
