# Xcode Setup - Name and Testing Options

## 📝 Widget Name

### Product Name (Technical/Internal)
**Use**: `PDFMonitorWidget` (keep it short, no spaces)

**Why?**
- This is the internal name Xcode uses
- No spaces or special characters
- Used for file names and code references
- Shorter is better for technical names

### Display Name (What Users See)
**Can be**: `PDF OCR Monitor Widget` (more descriptive)

**How to set:**
- After creating project, go to project settings
- Find "Display Name" field
- Set to: `PDF OCR Monitor Widget`
- This is what appears in Notification Center

**Recommendation:**
- Product Name: `PDFMonitorWidget` ✅
- Display Name: `PDF OCR Monitor Widget` ✅ (set after creation)

## 🧪 Testing System

### What is "Testing System"?
This asks what testing framework to include in your project.

### Options:
1. **None** ✅ **Choose this!**
   - No test files created
   - Perfect for simple widgets
   - Faster setup
   - You can add tests later if needed

2. **XCTest for Unit and UI Tests**
   - Creates test files
   - For writing unit tests
   - Not needed for basic widget

3. **Swift Testing with XCTest UI Tests**
   - Newer testing framework
   - More advanced
   - Not needed for basic widget

### Recommendation: **Choose "None"** ✅

**Why?**
- Widget is simple - no complex logic to test
- You can add tests later if needed
- Keeps project clean and simple
- Faster to set up

## 📋 Complete Setup Checklist

When creating project:

- **Product Name**: `PDFMonitorWidget` ✅
- **Team**: Your team (or None)
- **Organization Identifier**: `com.yourname` (or `com.pdfmonitor`)
- **Language**: **Swift** ✅
- **Interface**: **SwiftUI** ✅
- **Storage**: **None** ✅
- **Testing System**: **None** ✅ (recommended)

## 🎯 After Project Creation

1. **Set Display Name** (optional but recommended):
   - Click project in left sidebar
   - Select target: `PDFMonitorWidget`
   - Go to "General" tab
   - Find "Display Name" field
   - Set to: `PDF OCR Monitor Widget`

2. **Continue with widget extension setup**

## ✅ Summary

- **Product Name**: `PDFMonitorWidget` (keep it)
- **Display Name**: Set to `PDF OCR Monitor Widget` later (optional)
- **Testing System**: **None** (choose this)

