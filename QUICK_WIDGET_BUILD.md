# Quick Widget Build - Cheat Sheet

## 🎯 Goal
Create a Notification Center widget that shows PDF Monitor status

## ⚡ Super Quick Steps

### 1. Create Project (2 minutes)
```
Xcode → File → New → Project
→ macOS → App
→ Name: PDFMonitorWidget
→ Swift + SwiftUI
→ Save in: OCR_folder_app folder
```

### 2. Add Widget Extension (1 minute)
```
File → New → Target
→ Widget Extension
→ Name: PDFMonitorWidgetExtension
→ Uncheck "Include Configuration Intent"
→ Activate scheme
```

### 3. Copy Code (30 seconds)
```
Open: PDFMonitorWidgetExtension.swift (in Xcode)
Select All → Delete
Copy from: PDFMonitorWidgetExtension.swift (in OCR_folder_app)
Paste → Save
```

### 4. Build & Run (1 minute)
```
Select scheme: PDFMonitorWidgetExtension (top toolbar)
Press: Cmd+R
Widget appears in Notification Center!
```

### 5. Add to Notification Center (30 seconds)
```
Swipe right from right edge
→ Scroll down → "Edit Widgets"
→ Find "PDF Monitor" → Click "+"
→ Choose size → Done
```

## ✅ Total Time: ~5 minutes!

## 🎨 What You'll Get

A beautiful widget showing:
- ✅ Status (ON/OFF) with color indicator
- ✅ Folder name being monitored
- ✅ Statistics (processed files, errors)
- ✅ Auto-updates every 10 seconds

## 🐛 Common Issues

**Build fails?**
- Make sure you selected **PDFMonitorWidgetExtension** scheme
- Check deployment target is macOS 11.0+

**Widget doesn't appear?**
- Make sure you built the **Extension** target, not the main app
- Try Product → Clean Build Folder

**Can't find widget?**
- Swipe right from right edge of trackpad
- Or click date/time in menu bar
- Scroll to bottom → Edit Widgets

## 📝 Files You Need

- ✅ `PDFMonitorWidgetExtension.swift` - Widget code (already created)
- ✅ `BUILD_WIDGET_STEPS.md` - Detailed guide
- ✅ `widget_config.json` - Config file (created by widget app)

## 🚀 Ready? Let's Go!

1. Xcode should be opening now
2. Follow steps above
3. Widget will be ready in 5 minutes!

