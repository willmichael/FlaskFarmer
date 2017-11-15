//
//  PreviewViewController.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/13/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit
import QuickLook

class PreviewViewController: UIViewController, QLPreviewControllerDataSource {

    var fileURL:URL? = nil
    let qlControl = QLPreviewController()

    override func viewDidLoad() {
        super.viewDidLoad()
        self.qlControl.dataSource = self
        // Do any additional setup after loading the view, typically from a nib.
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    func numberOfPreviewItems(in controller: QLPreviewController) -> Int {
        return 1
    }
    
    func previewController(_ controller: QLPreviewController, previewItemAt index: Int) -> QLPreviewItem {
        return fileURL! as NSURL
    }
}
