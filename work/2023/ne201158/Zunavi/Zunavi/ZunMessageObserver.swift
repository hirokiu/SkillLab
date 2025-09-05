//
//  ZunMessageObserver.swift
//  Zunavi
//
//  Created by Futa Matsuo on 2023/09/08.
//

import Foundation
import AVFoundation

class ZunMessageObserver: ObservableObject {
    private var zunUsecase = CommunicateZunUsecase()
    @Published var messages: [Message] = []
    var musicPlayer: AVAudioPlayer!
    
    func connect() {
        zunUsecase.connect { (result) in
            DispatchQueue.main.async {
                switch result {
                case .failure(let error):
                    print("Error failed to receive message: \(error)")
                case .success(let message):
//                    do{
//                        self.musicPlayer = try AVAudioPlayer(data: message.file)
//                    } catch {
//                        print("音の再生に失敗しました")
//                    }
                    self.messages.append(message)
                }
            }
        }
    }
}
