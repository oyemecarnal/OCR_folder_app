# Install Xcode for WidgetKit Widget

## ✅ Current Status
- ✅ Command Line Tools: **Installed**
- ❌ Full Xcode.app: **Not installed** (needed for WidgetKit)

## 🚀 Install Xcode (Full Version)

### Step 1: Open App Store
1. Click the **Apple menu** (🍎) → **App Store**
2. Or press **Cmd+Space** and type "App Store"

### Step 2: Search for Xcode
1. In App Store, click the **Search** tab
2. Type **"Xcode"** in the search box
3. Press **Enter**

### Step 3: Install Xcode
1. Find **"Xcode"** by Apple (it's free)
2. Click **"Get"** or **"Install"** button
3. You may need to sign in with your Apple ID
4. Wait for download (this is **large** - ~10-15 GB)
5. Installation takes 15-30 minutes depending on internet speed

### Step 4: Accept License
After installation:
1. Open **Xcode** from Applications
2. Accept the license agreement
3. Let it install additional components (takes a few more minutes)

### Step 5: Verify Installation
Run this command to verify:
```bash
xcodebuild -version
```

You should see something like:
```
Xcode 15.0
Build version 15A240d
```

## ⚠️ Important Notes

- **Size**: Xcode is ~10-15 GB, make sure you have space
- **Time**: Download and install can take 30-60 minutes
- **Free**: Xcode is free from App Store (no payment needed)
- **Apple ID**: You'll need to sign in with your Apple ID

## 🔄 Alternative: Use Menu Bar Widget Instead

If you don't want to wait for Xcode installation, you can use the **Menu Bar Widget** instead:
- ✅ No Xcode needed
- ✅ Works immediately
- ✅ Always visible in menu bar
- ✅ Same functionality

To use Menu Bar Widget:
```bash
open PDFMonitorMenuBar.app
```

## 📋 After Xcode is Installed

Once Xcode is installed, follow:
1. `CREATE_WIDGETKIT_WIDGET.md` - Step-by-step guide to create the widget
2. Build the widget in Xcode
3. Add it to Notification Center

## 🆘 Troubleshooting

### App Store won't open
- Try: `open -a "App Store"`
- Or manually open App Store from Applications

### Download is slow
- Xcode is very large, be patient
- Check your internet connection
- Pause and resume if needed

### Installation fails
- Make sure you have enough disk space (15+ GB free)
- Check System Settings → General → Storage
- Free up space if needed

### Can't sign in to App Store
- Make sure you're signed in to App Store
- System Settings → Apple ID → Sign In

## ✅ Quick Check

After installation, verify with:
```bash
# Check Xcode is installed
ls -d /Applications/Xcode.app

# Check version
xcodebuild -version

# Check Swift is available
swift --version
```

All three commands should work if Xcode is properly installed!

