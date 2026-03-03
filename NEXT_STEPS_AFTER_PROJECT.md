# Next Steps After Creating Xcode Project

## 📍 Step 1: Open Your Project

### Option A: From Finder
1. Open **Finder**
2. Navigate to: `/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/`
3. Look for: `PDFMonitorWidget.xcodeproj`
4. **Double-click** it to open in Xcode

### Option B: From Xcode
1. Open **Xcode**
2. **File** → **Open** (or **Cmd+O**)
3. Navigate to: `OCR_folder_app` folder
4. Select `PDFMonitorWidget.xcodeproj`
5. Click **Open**

### Option C: Recent Projects
1. Open **Xcode**
2. **File** → **Open Recent**
3. Look for `PDFMonitorWidget`
4. Click it

## ✅ Step 2: Verify Project is Open

You should see:
- Project name `PDFMonitorWidget` in left sidebar
- Files like `App.swift` or `ContentView.swift`
- Project settings in main area

## 🚀 Step 3: Add Widget Extension

### 3.1 Add Target
1. **File** → **New** → **Target** (or press **Cmd+Option+N**)
2. In the template chooser:
   - Choose **"Widget Extension"** (under macOS section)
   - Click **Next**

### 3.2 Configure Extension
- **Product Name**: `PDFMonitorWidgetExtension`
- **Team**: Same as main app (or None)
- **Organization Identifier**: Same as main app
- **Language**: **Swift**
- **Include Configuration Intent**: **Unchecked** ✅ (important!)
- Click **Finish**

### 3.3 Activate Scheme
- When prompted: **"Activate 'PDFMonitorWidgetExtension' scheme?"**
- Click **Activate** ✅

## 📝 Step 4: Add Widget Code

### 4.1 Find Widget File
1. In left sidebar, expand `PDFMonitorWidgetExtension` folder
2. Find `PDFMonitorWidgetExtension.swift` file
3. Click it to open

### 4.2 Replace Code
1. **Select All** (Cmd+A)
2. **Delete** (Backspace)
3. Open the file: `PDFMonitorWidgetExtension.swift` from your OCR_folder_app folder
4. **Copy All** (Cmd+A, then Cmd+C)
5. Go back to Xcode
6. **Paste** (Cmd+V)
7. **Save** (Cmd+S)

## 🔨 Step 5: Build and Run

### 5.1 Select Scheme
- At top toolbar, click the scheme dropdown
- Select **"PDFMonitorWidgetExtension"** (NOT the main app)

### 5.2 Build
- Press **Cmd+B** to build
- Wait for "Build Succeeded" ✅

### 5.3 Run
- Press **Cmd+R** to run
- Widget should appear in Notification Center!

## 📱 Step 6: Add to Notification Center

1. **Swipe right** from right edge of trackpad
   - Or click **date/time** in menu bar
2. Scroll to bottom
3. Click **"Edit Widgets"**
4. Find **"PDF Monitor"** in the list
5. Click **"+"** button
6. Choose size: **Small** or **Medium**
7. Click **"Done"**

## ✅ Checklist

- [ ] Project opened in Xcode
- [ ] Widget Extension target added
- [ ] Code copied to extension file
- [ ] Build successful (no errors)
- [ ] Widget runs and appears
- [ ] Widget added to Notification Center

## 🐛 Troubleshooting

### Can't find project?
- Check where you saved it when creating
- Look in Documents or Desktop
- Use Finder search for "PDFMonitorWidget.xcodeproj"

### Build errors?
- Make sure you selected **PDFMonitorWidgetExtension** scheme
- Check deployment target is macOS 11.0+
- Try: **Product** → **Clean Build Folder** (Cmd+Shift+K)

### Widget doesn't appear?
- Make sure you built the **Extension** target, not main app
- Check scheme is set to PDFMonitorWidgetExtension
- Try running again (Cmd+R)

## 🎉 You're Almost There!

Once you open the project, follow steps 3-6 above. The widget will be ready in just a few minutes!

