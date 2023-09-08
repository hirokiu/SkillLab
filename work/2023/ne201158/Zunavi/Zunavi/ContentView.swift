//
//  ContentView.swift
//  Zunavi
//
//  Created by Futa Matsuo on 2023/09/07.
//

import SwiftUI
import CoreData

struct ContentView: View {
    @EnvironmentObject var messageObserver: ZunMessageObserver
    @EnvironmentObject var locationManager: LocationManager

    var body: some View {
        NavigationView {
            List {
                ForEach(messageObserver.messages, id: \.id) { message in
                    VStack(alignment: .leading) {
                        Text(message.text)
                    }
                }
            }.navigationTitle("Messages")
        }
        .onAppear {
            messageObserver.connect()
            locationManager.startSendingLocation()
        }
    }

}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView().environmentObject(ZunMessageObserver())
    }
}

