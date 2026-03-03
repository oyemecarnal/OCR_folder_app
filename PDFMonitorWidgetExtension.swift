//
// PDFMonitorWidgetExtension.swift
// macOS WidgetKit Extension for PDF Monitor
// Shows status in Notification Center
//

import WidgetKit
import SwiftUI

struct PDFMonitorWidget: Widget {
    let kind: String = "PDFMonitorWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: PDFMonitorProvider()) { entry in
            PDFMonitorWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("PDF Monitor")
        .description("Monitor and process PDFs with OCR")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct PDFMonitorProvider: TimelineProvider {
    func placeholder(in context: Context) -> PDFMonitorEntry {
        PDFMonitorEntry(
            date: Date(),
            status: "off",
            folder: "No folder",
            processed: 0,
            errors: 0
        )
    }

    func getSnapshot(in context: Context, completion: @escaping (PDFMonitorEntry) -> ()) {
        let entry = PDFMonitorEntry(
            date: Date(),
            status: loadStatus(),
            folder: loadFolder(),
            processed: loadProcessed(),
            errors: loadErrors()
        )
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        let entry = PDFMonitorEntry(
            date: Date(),
            status: loadStatus(),
            folder: loadFolder(),
            processed: loadProcessed(),
            errors: loadErrors()
        )
        
        // Update every 10 seconds
        let nextUpdate = Calendar.current.date(byAdding: .second, value: 10, to: Date())!
        let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))
        completion(timeline)
    }
    
    func loadStatus() -> String {
        // Read from config file in OCR_folder_app
        let configPath = "/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/widget_config.json"
        
        if let data = try? Data(contentsOf: URL(fileURLWithPath: configPath)),
           let config = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
           let monitoring = config["monitoring"] as? Bool {
            return monitoring ? "on" : "off"
        }
        return "off"
    }
    
    func loadFolder() -> String {
        let configPath = "/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/widget_config.json"
        
        if let data = try? Data(contentsOf: URL(fileURLWithPath: configPath)),
           let config = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
           let folder = config["folder"] as? String,
           !folder.isEmpty {
            // Return just the folder name, not full path
            return (folder as NSString).lastPathComponent
        }
        return "No folder"
    }
    
    func loadProcessed() -> Int {
        // Try to read from stats file if it exists
        let statsPath = "/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/monitor_stats.json"
        
        if let data = try? Data(contentsOf: URL(fileURLWithPath: statsPath)),
           let stats = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
           let processed = stats["total_processed"] as? Int {
            return processed
        }
        return 0
    }
    
    func loadErrors() -> Int {
        let statsPath = "/Users/kevinreed/Library/CloudStorage/OneDrive-Personal/OCR_folder_app/monitor_stats.json"
        
        if let data = try? Data(contentsOf: URL(fileURLWithPath: statsPath)),
           let stats = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
           let errors = stats["total_errors"] as? Int {
            return errors
        }
        return 0
    }
}

struct PDFMonitorEntry: TimelineEntry {
    let date: Date
    let status: String
    let folder: String
    let processed: Int
    let errors: Int
}

struct PDFMonitorWidgetEntryView: View {
    var entry: PDFMonitorProvider.Entry
    
    var statusColor: Color {
        entry.status == "on" ? .green : .red
    }
    
    var statusSymbol: String {
        entry.status == "on" ? "✓" : "○"
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            // Header with status indicator
            HStack {
                Text("PDF Monitor")
                    .font(.headline)
                    .fontWeight(.semibold)
                    .foregroundColor(.primary)
                
                Spacer()
                
                // Status circle
                ZStack {
                    Circle()
                        .fill(statusColor.opacity(0.2))
                        .frame(width: 24, height: 24)
                    Text(statusSymbol)
                        .font(.system(size: 12, weight: .bold))
                        .foregroundColor(statusColor)
                }
            }
            
            Divider()
            
            // Status text
            HStack {
                Text(entry.status.uppercased())
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(statusColor)
                Spacer()
            }
            
            // Folder name
            HStack {
                Image(systemName: "folder.fill")
                    .foregroundColor(.secondary)
                    .font(.caption)
                Text(entry.folder)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
                Spacer()
            }
            
            // Statistics
            HStack(spacing: 20) {
                VStack(alignment: .leading, spacing: 2) {
                    Text("\(entry.processed)")
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(statusColor)
                    Text("Processed")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                VStack(alignment: .trailing, spacing: 2) {
                    Text("\(entry.errors)")
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(.red)
                    Text("Errors")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }
            .padding(.top, 4)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color(NSColor.controlBackgroundColor))
    }
}

@main
struct PDFMonitorWidgetBundle: WidgetBundle {
    var body: some Widget {
        PDFMonitorWidget()
    }
}
