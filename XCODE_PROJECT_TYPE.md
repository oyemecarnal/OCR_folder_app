# Xcode Project Type - Choose "App" (Not Document App)

## ✅ Correct Choice: **App**

When creating the project in Xcode:

1. **macOS** tab (at the top)
2. Select **"App"** (NOT "Document App")
3. Click **Next**

## ❌ Don't Choose: Document App

**Document App** is for apps that:
- Work with document files
- Have document-based architecture
- Open/save documents
- Not needed for widgets

## ✅ Choose: App

**App** is for:
- Regular macOS applications
- Widget extensions (what we need!)
- Menu bar apps
- Standard apps

## 📋 Step-by-Step in Xcode

1. **File** → **New** → **Project**
2. **macOS** tab (top)
3. Select **"App"** template (first option, has app icon)
4. Click **Next**
5. Fill in:
   - Product Name: `PDFMonitorWidget`
   - Team: Your team
   - Organization Identifier: `com.yourname`
   - Language: **Swift**
   - Interface: **SwiftUI**
   - Storage: **None**
6. Click **Next** → **Create**

## 🎯 Why "App"?

WidgetKit extensions need to be added to a regular macOS App target. The main app doesn't need to do anything - it's just a container for the widget extension. The widget extension is what actually runs in Notification Center.

## ✅ Summary

- **Choose**: **App** ✅
- **Don't choose**: Document App ❌

That's it! Simple choice.

