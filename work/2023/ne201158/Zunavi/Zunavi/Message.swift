//
//  Message.swift
//  Zunavi
//
//  Created by Futa Matsuo on 2023/09/08.
//

import Foundation

struct Message: Codable {
    let id: String
    let text: String
}

enum MessageDecodingError: Error {
    case dataConversionFailed
    case decodingFailed(Error)
}

func decodeJSONtoMessage(from textMessage: String) throws -> Message {
    guard let data = textMessage.data(using: .utf8) else {
        throw MessageDecodingError.dataConversionFailed
    }
    do {
        let decodedMessage = try JSONDecoder().decode(Message.self, from: data)
        return decodedMessage
    } catch let decodingError {
        throw MessageDecodingError.decodingFailed(decodingError)
    }
}

