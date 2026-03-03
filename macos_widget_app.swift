#!/usr/bin/env swift
//
// PDF Monitor macOS Widget App
// Simple SwiftUI app that displays the widget interface
//

import SwiftUI
import AppKit
import Combine

@main
struct PDFMonitorWidgetApp: App {
    var body: some Scene {
        WindowGroup {
            WidgetView()
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
    }
}

struct WidgetView: View {
    @State private var status: String = "off"
    @State private var processed: Int = 0
    @State private var errors: Int = 0
    @State private var isLoading: Bool = true
    
    let timer = Timer.publish(every: 10, on: .main, in: .common).autoconnect()
    
    var statusColor: Color {
        status == "on" ? .green : .red
    }
    
    var body: some View {
        VStack(spacing: 20) {
            // Status Indicator
            ZStack {
                Circle()
                    .fill(statusColor.opacity(0.2))
                    .frame(width: 80, height: 80)
                Circle()
                    .stroke(statusColor, lineWidth: 3)
                    .frame(width: 80, height: 80)
                Text(status == "on" ? "✓" : "○")
                    .font(.system(size: 40))
                    .foregroundColor(statusColor)
            }
            
            // Status Text
            Text(status.uppercased())
                .font(.system(size: 32, weight: .bold))
                .foregroundColor(statusColor)
            
            Text("PDF Monitor")
                .font(.system(size: 14))
                .foregroundColor(.secondary)
            
            // Statistics
            HStack(spacing: 15) {
                StatBox(value: processed, label: "Processed", color: statusColor)
                StatBox(value: errors, label: "Errors", color: .red)
            }
            
            // Control Buttons
            HStack(spacing: 10) {
                Button(action: toggleMonitor) {
                    Text("Toggle")
                        .frame(width: 100)
                        .padding(.vertical, 8)
                }
                .buttonStyle(.borderedProminent)
                .tint(statusColor)
                
                Button(action: status == "on" ? turnOff : turnOn) {
                    Text(status == "on" ? "Turn OFF" : "Turn ON")
                        .frame(width: 100)
                        .padding(.vertical, 8)
                }
                .buttonStyle(.bordered)
            }
            
            if isLoading {
                ProgressView()
                    .scaleEffect(0.8)
            }
        }
        .padding(30)
        .frame(width: 350, height: 450)
        .background(Color(NSColor.windowBackgroundColor))
        .onAppear {
            fetchStatus()
        }
        .onReceive(timer) { _ in
            fetchStatus()
        }
    }
    
    func fetchStatus() {
        guard let url = URL(string: "http://localhost:5002/api/status") else { return }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let data = data,
               let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let statusData = json["status"] as? String,
               let stats = json["stats"] as? [String: Any] {
                DispatchQueue.main.async {
                    self.status = statusData
                    self.processed = stats["processed"] as? Int ?? 0
                    self.errors = stats["errors"] as? Int ?? 0
                    self.isLoading = false
                }
            }
        }.resume()
    }
    
    func toggleMonitor() {
        sendCommand(endpoint: "/api/toggle")
    }
    
    func turnOn() {
        sendCommand(endpoint: "/api/on")
    }
    
    func turnOff() {
        sendCommand(endpoint: "/api/off")
    }
    
    func sendCommand(endpoint: String) {
        guard let url = URL(string: "http://localhost:5002\(endpoint)") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        URLSession.shared.dataTask(with: request) { _, _, _ in
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                fetchStatus()
            }
        }.resume()
    }
}

struct StatBox: View {
    let value: Int
    let label: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 5) {
            Text("\(value)")
                .font(.system(size: 24, weight: .bold))
                .foregroundColor(color)
            Text(label)
                .font(.system(size: 12))
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(12)
    }
}

