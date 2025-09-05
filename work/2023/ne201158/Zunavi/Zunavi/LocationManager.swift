//
//  LocationManager.swift
//  Zunavi
//
//  Created by 犬寄ふのぶ on 2023/09/08.
//

import Foundation
import CoreLocation

class LocationManager: NSObject, ObservableObject, CLLocationManagerDelegate {
    private var locationManager = CLLocationManager()
    private var targetURL = URL(string: "http://localhost:8036/geo")!

    override init() {
        super.init()
        self.locationManager.delegate = self
        self.locationManager.requestWhenInUseAuthorization()
        self.locationManager.startUpdatingLocation()
    }

    func startSendingLocation() {
        locationManager.requestWhenInUseAuthorization()
        Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { timer in
            self.sendLocation()
        }
    }

    func sendLocation() {
        guard let location = locationManager.location else {
            print("No location available")
            return
        }
        
        var request = URLRequest(url: targetURL)
        request.httpMethod = "POST"
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")

        let bodyData = "lat=\(location.coordinate.latitude)&lng=\(location.coordinate.longitude)"
        request.httpBody = bodyData.data(using: .utf8)
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Error: \(error?.localizedDescription ?? "No data")")
                return
            }
            print("Response: \(String(data: data, encoding: .utf8) ?? "")")
        }
        task.resume()
    }
}
