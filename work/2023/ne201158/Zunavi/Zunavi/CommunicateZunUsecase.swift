//
//  CommunicateZunUsecase.swift
//  Zunavi
//
//  Created by Futa Matsuo on 2023/09/08.
//

import Foundation

class CommunicateZunUsecase {
    private let urlSession = URLSession(configuration: .default)
    private var websocketTask: URLSessionWebSocketTask?
    // TODO: 本来は認可処理を実装した上で端末ごとにアクセスするURLを変える必要がある。
    private let targetURL = URL(string: "ws://localhost:8035/zunavi/1")!
    private var reconnectTimer: Timer?
    private var lastOnMessageReceived: ((Result<Message, Error>) -> Void)?
    
    
    func stop() {
        websocketTask?.cancel(with: .goingAway, reason: nil)
    }
    
    private func sendPing() {
        websocketTask?.sendPing { (error) in
            if let error = error {
                print("Error cannot send PING; \(error)")
            }
            
            DispatchQueue.main.asyncAfter(deadline: .now() + 10) { [weak self] in
                self?.sendPing()
            }
        }
    }
    
//    private func attemptReconnect() {
//        guard websocketTask?.state != .running else {
//            reconnectTimer?.invalidate()
//            reconnectTimer = nil
//            return
//        }
//
//        guard let lastOnMessageReceived = lastOnMessageReceived else {
//        // Handle the error: No callback to reuse for message receiving
//            print("connection failed")
//            return
//        }
//
//        connect(onMessageReceived: lastOnMessageReceived)
//    }
//
//    private func startReconnectTimer() {
//        reconnectTimer?.invalidate()
//        reconnectTimer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { [weak self] _ in
//            self?.attemptReconnect()
//        }
//    }
    
    func onReceivedZundamonMessage(completionHandler: @escaping (Result<Message, Error>) -> Void) {
        websocketTask?.receive {[weak self] result in
            switch result {
            case .failure(let error):
                print("Error cannot send PING; \(error)")
            case .success(let message):
                switch message {
                case .string(let textMessage):
                    do {
                        let decodedmessage = try decodeJSONtoMessage(from: textMessage)
                        completionHandler(.success(decodedmessage))
                    } catch {
                        completionHandler(.failure(NSError(domain: "failed to convert JSON", code: -1)))
                    }
                default:
                    completionHandler(.failure(NSError(domain: "failed to fetch data", code: -1)))
                }
                self?.onReceivedZundamonMessage(completionHandler: completionHandler)
            }
        }
    }
    
    func connect(onMessageReceived: @escaping (Result<Message, Error>) -> Void) {
        stop()
        websocketTask = urlSession.webSocketTask(with: targetURL)
        websocketTask?.resume()
        
        sendPing()
        onReceivedZundamonMessage(completionHandler: onMessageReceived)
    }
}
