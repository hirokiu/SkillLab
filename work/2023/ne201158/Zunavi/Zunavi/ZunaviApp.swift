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

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(messageObserver)
        }
    }
}
