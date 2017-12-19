//
//  MainViewController.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/2/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit

class MainViewController: UIViewController, UIDocumentPickerDelegate {


    @IBOutlet weak var controlOutletButton: UIButton!
    // Mark Properties
    @IBOutlet weak var changeText: UILabel!
    var documentController : UIDocumentInteractionController!
    var isOn = false

    // File Properties
    let tmpDirURL = NSURL.init(fileURLWithPath: NSTemporaryDirectory())
    let fileName = "test.csv"
    let excelFileName = "excel_test.xlsx"
    let documentURL = NSURL.init(fileURLWithPath: NSHomeDirectory())

    let fileManager = FileManager.default



    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Home"

        // Do any additional setup after loading the view.
    }

    @IBAction func listDocuments(_ sender: Any) {
        do {
            let documentDirectory = try self.fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor:nil, create:false)
            let directoryContents = try self.fileManager.contentsOfDirectory(at: documentDirectory, includingPropertiesForKeys: nil, options: [])
            print(directoryContents)
        } catch {
            print("listing error")
        }
    }

    @IBAction func getExcelFile(_ sender: Any) {
        isOn = !isOn
        if isOn {
            changeText.text = "on"
            downloadExcelFileFromServer()
        } else {
            changeText.text = "off"
            print("nothing")
        }
    }

    @IBAction func getFile(_ sender: Any) {
        isOn = !isOn
        if isOn {
            changeText.text = "on"
            downloadFileFromServer()
        } else {
            changeText.text = "off"
            print("nothing")
        }
    }

    @IBAction func controlFile(_ sender: Any) {
        let targetURL = self.documentURL.appendingPathComponent(self.fileName)
        print(targetURL!)
        documentController = UIDocumentInteractionController.init(url: targetURL!)
        documentController.presentOptionsMenu(from: self.controlOutletButton.frame, in: self.view, animated: true)
    }
    // Save excel file to dir
    func downloadExcelFileFromServer() -> Void {
        let json = ["user":"larry"]

        do {
            let jsonData = try JSONSerialization.data(withJSONObject: json, options: .prettyPrinted)

            let url = NSURL(string: "http://138.68.224.118:5000/api/get_excel_file")!
            let request = NSMutableURLRequest(url: url as URL)
            request.httpMethod = "POST"

            request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData

            let task = URLSession.shared.dataTask(with: request as URLRequest){ data, response, error in
                if error != nil{
                    print("Error -> \(String(describing: error))")
                    return
                }
                do {
                    let documentDirectory = try self.fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor:nil, create:false)
                    let fileURL = documentDirectory.appendingPathComponent(self.excelFileName)
                    print("Target URL -> \(fileURL)")
                    try data!.write(to: fileURL)

                } catch {
                    print("Error -> \(error)")
                }
            }
            task.resume()
        } catch {
            print(error)
        }
    }

    // Save file to dir
    func downloadFileFromServer() -> Void {
        let json = ["user":"larry"]

        do {
            let jsonData = try JSONSerialization.data(withJSONObject: json, options: .prettyPrinted)

            let url = NSURL(string: "http://138.68.224.118:5000/api/get_file")!
            let request = NSMutableURLRequest(url: url as URL)
            request.httpMethod = "POST"

            request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData

            let task = URLSession.shared.dataTask(with: request as URLRequest){ data, response, error in
                if error != nil{
                    print("Error -> \(String(describing: error))")
                    return
                }
                do {
                    let documentDirectory = try self.fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor:nil, create:false)
                    let fileURL = documentDirectory.appendingPathComponent(self.fileName)
//                    if let filePath = NSBundle.mainBundle().pathForResource(fileURL, ofType: "csv"){
//
//                    }
                    print("Target URL -> \(fileURL)")
                    try data!.write(to: fileURL)
//                    print("Received -> \(String(describing: data))")
//                    print("respondse -> \(String(describing: response))")
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
