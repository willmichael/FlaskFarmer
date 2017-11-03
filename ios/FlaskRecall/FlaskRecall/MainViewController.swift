//
//  MainViewController.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/2/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit

class MainViewController: UIViewController {


    @IBOutlet weak var changeText: UILabel!
    var isOn = false

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    @IBAction func getFile(_ sender: Any) {
        isOn = !isOn
        if isOn {
            changeText.text = "on"
            printMessagesForUser()
        } else {
            changeText.text = "off"
            print("nothing")
        }
    }

    func printMessagesForUser() -> Void {
        let json = ["user":"larry"]

        do {
            let jsonData = try JSONSerialization.data(withJSONObject: json, options: .prettyPrinted)

            let url = NSURL(string: "http://127.0.0.1:5000/api/get_messages")!
            let request = NSMutableURLRequest(url: url as URL)
            request.httpMethod = "POST"

            request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData

            let task = URLSession.shared.dataTask(with: request as URLRequest){ data, response, error in
                if error != nil{
                    print("Error -> \(error)")
                    return
                }
                do {
                    let result = try JSONSerialization.jsonObject(with: data!, options: .allowFragments) as? [String:AnyObject]
                    print("Result -> \(result)")

                } catch {
                    print("Error -> \(error)")
                }
            }

            task.resume()
        } catch {
            print(error)
        }
    }

}
