# Build Notification Center Widget - Step by Step

## ✅ Prerequisites
- ✅ Xcode installed
- ✅ macOS 11.0+ (Big Sur or later)

## 🚀 Step-by-Step Instructions

### Step 1: Create New Xcode Project

1. **Open Xcode**
   - Press **Cmd+Space**, type "Xcode", press Enter
   - Or open from Applications

2. **Create New Project**
   - **File** → **New** → **Project** (or press **Cmd+Shift+N**)
   - Choose **"macOS"** tab (at the top)
   - Select **"App"** template
   - Click **Next**

3. **Configure Project**
   - **Product Name**: `PDFMonitorWidget`
   - **Team**: Select your team (or "None" if you don't have one)
   - **Organization Identifier**: `com.yourname` (or use `com.pdfmonitor`)
   - **Bundle Identifier**: Will auto-fill as `com.yourname.PDFMonitorWidget`
   - **Language**: **Swift**
   - **Interface**: **SwiftUI**
   - **Storage**: **None**
   - **Use Core Data**: **Unchecked**
   - **Include Tests**: **Unchecked** (optional)
   - Click **Next**

4. **Choose Location**
   - Navigate to: `/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/`
   - Click **Create**

### Step 2: Add Widget Extension Target

1. **Add New Target**
   - **File** → **New** → **Target** (or press **Cmd+Option+N**)
   - Choose **"Widget Extension"** (under macOS)
   - Click **Next**

2. **Configure Widget Extension**
   - **Product Name**: `PDFMonitorWidgetExtension`
   - **Team**: Same as main app
   - **Organization Identifier**: Same as main app
   - **Bundle Identifier**: Will auto-fill
   - **Language**: **Swift**
   - **Include Configuration Intent**: **Unchecked** (we don't need this)
   - Click **Finish**

3. **Activate Scheme**
   - When prompted "Activate 'PDFMonitorWidgetExtension' scheme?", click **Activate**

### Step 3: Add Widget Code

1. **Find the Widget File**
   - In Xcode's left sidebar (Project Navigator), find:
     - `PDFMonitorWidgetExtension` folder
     - `PDFMonitorWidgetExtension.swift` file

2. **Replace the Code**
   - Click on `PDFMonitorWidgetExtension.swift`
   - **Select All** (Cmd+A)
   - **Delete** (Backspace)
   - **Copy** the code from `PDFMonitorWidgetExtension.swift` in your OCR_folder_app folder
   - **Paste** it into Xcode
   - **Save** (Cmd+S)

### Step 4: Update Info.plist (if needed)

1. **Find Info.plist**
   - In `PDFMonitorWidgetExtension` target
   - Look for `Info.plist` file

2. **Add Key** (if not present)
   - Right-click → **Add Row**
   - Key: `NSSupportsAutomaticGraphicsSwitching`
   - Type: **Boolean**
   - Value: **YES** (checked)

### Step 5: Build and Run

1. **Select Scheme**
   - At the top toolbar, click the scheme dropdown (next to the play/stop buttons)
   - Select **"PDFMonitorWidgetExtension"** (not the main app)

2. **Build**
   - Press **Cmd+B** to build
   - Wait for build to complete
   - Fix any errors if they appear

3. **Run**
   - Press **Cmd+R** to run
   - Widget should appear in Notification Center!

### Step 6: Add Widget to Notification Center

1. **Open Notification Center**
   - **Swipe right** from the right edge of your trackpad
   - Or click the **date/time** in the menu bar

2. **Edit Widgets**
   - Scroll to the bottom
   - Click **"Edit Widgets"** button

3. **Add PDF Monitor Widget**
   - Find **"PDF Monitor"** in the widget list
   - Click the **"+"** button next to it
   - Choose size: **Small** or **Medium**
   - Click **"Done"**

4. **View Your Widget**
   - Swipe right to open Notification Center
   - Your PDF Monitor widget should be there!

## 🎨 Widget Features

- **Status Display**: Shows ON/OFF with color indicator
- **Folder Name**: Shows which folder is being monitored
- **Statistics**: Shows processed files and errors
- **Auto-Update**: Refreshes every 10 seconds

## 🔧 Configuration

The widget reads from `widget_config.json` in your OCR_folder_app folder:
- `monitoring`: true/false (ON/OFF status)
- `folder`: Path to monitored folder
- `max_age_hours`: Time threshold

## 🐛 Troubleshooting

### Build Errors

**"Cannot find type 'Widget' in scope"**
- Make sure you selected the **Widget Extension** target, not the main app
- Check that WidgetKit framework is imported

**"No such module 'WidgetKit'"**
- Make sure you're building for macOS 11.0+
- Check deployment target in project settings

### Widget Doesn't Appear

- Make sure you selected **PDFMonitorWidgetExtension** scheme
- Check that build succeeded (no errors)
- Try cleaning: **Product** → **Clean Build Folder** (Cmd+Shift+K)

### Widget Doesn't Update

- Widgets update on a schedule (every 10 seconds in our code)
- Pull down Notification Center to refresh
- Check that `widget_config.json` exists and is readable

### Can't Find Widget in Notification Center

- Make sure you built and ran the **Widget Extension** target
- Try removing and re-adding the widget
- Restart your Mac if needed

## ✅ Success Checklist

- [ ] Xcode project created
- [ ] Widget Extension target added
- [ ] Code copied to extension
- [ ] Build successful (no errors)
- [ ] Widget runs without crashing
- [ ] Widget appears in Notification Center
- [ ] Widget shows correct status
- [ ] Widget updates automatically

## 🎉 You're Done!

Your widget should now be in Notification Center! Swipe right from the right edge to see it.

## 📝 Next Steps

- Customize the widget appearance
- Add more information
- Adjust update frequency
- Add interaction (if needed)

