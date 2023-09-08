//
//  ZunaviApp.swift
//  Zunavi
//
//  Created by Futa Matsuo on 2023/09/07.
//

import SwiftUI

@main
struct ZunaviApp: App {
    let persistenceController = PersistenceController.shared
    @StateObject private var messageObserver = ZunMessageObserver()
    @StateObject private var locationManger = LocationManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(messageObserver)
                .environmentObject(locationManger)
        }
    }
}
