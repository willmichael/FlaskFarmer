//
//  StageController.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/22/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit

class StageController: UIViewController {
//    let tableView = UITableView()

    override func viewDidLoad() {
        super.viewDidLoad()
        let tableView = UITableView(frame: CGRect(x: 0, y: 0, width: view.frame.width, height: view.frame.height) , style:.grouped)

        view.addSubview(tableView)

        tableView.clipsToBounds = true
        tableView.delegate = self
        tableView.dataSource = self


    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }


}

extension StageController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = UITableViewCell()
        cell.textLabel?.text = String(indexPath.row)
        return cell
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 3
    }
}

extension StageController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        switch indexPath.row {
        case 1:
            return
        default:
            return
        }
    }

}
