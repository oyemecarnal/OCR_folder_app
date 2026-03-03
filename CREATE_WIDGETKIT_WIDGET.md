# Create macOS WidgetKit Widget - Step by Step

## 🎯 Goal
Add PDF Monitor to the macOS Notification Center widget panel (swipe right from right edge).

## ⚠️ Important Note
macOS WidgetKit widgets require:
- **Xcode** (free from App Store)
- **macOS 11.0+** (Big Sur or later)
- **Swift/SwiftUI** knowledge (or follow these steps exactly)

## 🚀 Method 1: Quick Setup with Xcode (Recommended)

### Step 1: Install Xcode
1. Open **App Store**
2. Search for **"Xcode"**
3. Click **"Get"** or **"Install"**
4. Wait for installation (this is large, ~10GB)

### Step 2: Create Widget Project
1. Open **Xcode**
2. **File** → **New** → **Project**
3. Choose **"macOS"** → **"App"**
4. Click **Next**
5. Fill in:
   - **Product Name**: `PDFMonitorWidget`
   - **Team**: (your Apple ID)
   - **Organization Identifier**: `com.yourname`
   - **Language**: **Swift**
   - **Interface**: **SwiftUI**
   - **Storage**: **None**
6. Click **Next**
7. Choose location and click **Create**

### Step 3: Add Widget Extension
1. **File** → **New** → **Target**
2. Choose **"Widget Extension"**
3. Click **Next**
4. Fill in:
   - **Product Name**: `PDFMonitorWidgetExtension`
   - **Include Configuration Intent**: **Unchecked**
5. Click **Finish**
6. Click **Activate** when prompted

### Step 4: Replace Widget Code
1. In Xcode, find `PDFMonitorWidgetExtension.swift` (in the Widget Extension folder)
2. **Delete** all the default code
3. **Copy and paste** the code from `PDFMonitorWidgetExtension.swift` in this folder
4. **Save** (Cmd+S)

### Step 5: Update Info.plist
1. Find `Info.plist` in the Widget Extension target
2. Add these keys if not present:
   ```xml
   <key>NSSupportsAutomaticGraphicsSwitching</key>
   <true/>
   ```

### Step 6: Build and Run
1. Select the **Widget Extension** scheme (top toolbar)
2. Press **Cmd+R** to build and run
3. Widget should appear in Notification Center!

### Step 7: Add to Notification Center
1. **Swipe right** from right edge of trackpad
2. Or click the **date/time** in menu bar
3. Scroll to bottom, click **"Edit Widgets"**
4. Find **"PDF Monitor"** in the list
5. Click **"+"** to add it
6. Choose size (Small or Medium)
7. Click **"Done"**

## 🔧 Method 2: Alternative - Menu Bar Widget

If WidgetKit is too complex, we can create a menu bar widget that's always accessible:

### Create Menu Bar Widget
This would be a simpler approach - a menu bar item that shows status and controls.

Would you like me to create this instead? It's much simpler and doesn't require Xcode.

## 📋 Requirements Checklist

- [ ] Xcode installed
- [ ] macOS 11.0+ (Big Sur or later)
- [ ] Widget Extension target created
- [ ] Code copied to extension
- [ ] Built successfully
- [ ] Added to Notification Center

## 🐛 Troubleshooting

### Widget doesn't appear
- Make sure you selected the **Widget Extension** scheme, not the main app
- Check that the widget is built for the correct macOS version
- Try cleaning build folder: **Product** → **Clean Build Folder**

### Widget doesn't update
- WidgetKit widgets update on a schedule (every 10 seconds in our code)
- Pull down Notification Center to refresh
- Check that `widget_config.json` is in the right location

### Build errors
- Make sure Swift version is 5.0+
- Check that all imports are available
- Verify Info.plist is configured correctly

## 💡 Simpler Alternative

If WidgetKit is too complex, I can create:
1. **Menu Bar Widget** - Always visible in menu bar
2. **Desktop Widget** - Floating window on desktop
3. **Dock Widget** - Quick access from Dock

Which would you prefer?

