//
//  PreviewViewController.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/13/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit
import QuickLook

class PreviewViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, QLPreviewControllerDataSource {


    @IBOutlet weak var tableView: UITableView!

    var fileURLs = [NSURL]()
    var fileNames = [String]()
    var fileExtensions = [String]()
    var fileURL:URL? = nil
    let qlControl = QLPreviewController()

    let fileManager = FileManager.default
    let excelFileName = "excel_test.xlsx"


    override func viewDidLoad() {
        super.viewDidLoad()
        print("inside preview view controller\n")
        getFileUrls()
        configureTable()
//        do {
//            let documentDirectory = try self.fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor:nil, create:false)
//            self.fileURL = documentDirectory.appendingPathComponent(self.excelFileName)
//        } catch {}
//
//        getFileUrls()
//
        self.qlControl.dataSource = self
//        self.present(qlControl, animated: true, completion: nil)
        // Do any additional setup after loading the view, typically from a nib.
    }


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    func configureTable() {
        tableView.delegate = self
        tableView.dataSource = self

    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
//        let cell = tableView.dequeueReusableCell(withIdentifier: "idCellFile", for: indexPath)
        let cell = UITableViewCell()
        cell.textLabel?.text = fileNames[indexPath.row]
        return cell
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        print(fileURLs.count)
        return fileURLs.count
    }

    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 80.0
    }

    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    func getFileUrls() {
        do {
            let documentDirectory = try self.fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor:nil, create:false)
            fileURLs = try self.fileManager.contentsOfDirectory(at: documentDirectory, includingPropertiesForKeys: nil, options: []) as [NSURL]

            for (n,file) in fileURLs.enumerated() {
                var name:String
                var ext:String

                (name, ext) = extractAndBreakFilenameInComponents(fileURL: file)
                fileNames.append(name)
                fileExtensions.append(ext)
            }
        } catch {
            print("Error: Could not get File URLS\n")
        }
    }

    func filterFileUrls() -> [NSURL]{
        var tempURLs = [NSURL]()
        for (n,name) in fileExtensions.enumerated() {
            if(name == "Inbox") {

            } else {
                tempURLs.append(fileURLs[n])
            }
        }
        return tempURLs
    }

    func extractAndBreakFilenameInComponents(fileURL: NSURL) -> (fileName: String, fileExtension: String) {
        // Break the NSURL path into its components and create a new array with those components.
        let fileURLParts = fileURL.path!.components(separatedBy: "/")
        // Get the file name from the last position of the array above.
        let fileName = fileURLParts.last
        // Break the file name into its components based on the period symbol (".").
        let filenameParts = fileName?.components(separatedBy: ".")
        // Return a tuple.
        if filenameParts!.count > 1 {
            return (filenameParts![0], filenameParts![1])
        } else {
            return (filenameParts![0], " ")
        }
    }

    func numberOfPreviewItems(in controller: QLPreviewController) -> Int {
        return fileURLs.count
    }
    
    func previewController(_ controller: QLPreviewController, previewItemAt index: Int) -> QLPreviewItem {
        return fileURLs[index]
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if QLPreviewController.canPreview(fileURLs[indexPath.row]) {
            qlControl.currentPreviewItemIndex = indexPath.row
            self.present(qlControl, animated: true, completion: nil)
        } else {
            print("cant preview")
        }
    }

}
