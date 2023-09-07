//
//  ZunMessageObserver.swift
//  Zunavi
//
//  Created by Futa Matsuo on 2023/09/08.
//

import Foundation

class ZunMessageObserver: ObservableObject {
    private var zunUsecase = CommunicateZunUsecase()
    @Published var messages: [Message] = []
    
    func connect() {
        zunUsecase.connect { (result) in
            DispatchQueue.main.async {
                switch result {
                case .failure(let error):
                    print("Error failed to receive message: \(error)")
                case .success(let message):
                    self.messages.append(message)
                }
            }
        }
    }
}
