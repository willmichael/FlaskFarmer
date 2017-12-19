//
//  RecallController.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/22/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit

class RecallController: UIViewController {

    let collectionView = UICollectionView(frame: CGRect(x: 0,
                                                        y: 0,
                                                        width: 0,
                                                        height: 0),
                                          collectionViewLayout: UICollectionViewFlowLayout())

    let cellReuse = "cellReuse"

    override func viewDidLoad() {
        super.viewDidLoad()

        title = "Recall"
        view.addSubview(collectionView)
        setupConstraints()
        collectionView.frame = CGRect(x: 0, y: 0, width: view.frame.width, height: view.frame.height)
        collectionView.backgroundColor = UIColor(white: 0.9, alpha: 1.0)

        collectionView.register(GenericRecallCell.self,
                                forCellWithReuseIdentifier: cellReuse)

        collectionView.dataSource = self
        collectionView.delegate = self

        let collectionViewLayout = UICollectionViewFlowLayout()
        collectionViewLayout.itemSize = CGSize(width: view.frame.width,
                                               height: (view.frame.height - 140) / 3)
        collectionViewLayout.minimumLineSpacing = 8
        collectionView.setCollectionViewLayout(collectionViewLayout,
                                               animated: false)

        // Do any additional setup after loading the view.
    }

    func setupConstraints() {
        collectionView.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            collectionView.topAnchor.constraint(equalTo: view.topAnchor),
            collectionView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            collectionView.leftAnchor.constraint(equalTo: view.leftAnchor),
            collectionView.rightAnchor.constraint(equalTo: view.rightAnchor)
            ])
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}


extension RecallController: UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 3
    }

    func collectionView(_ collectionView: UICollectionView,
                        cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {

        switch indexPath.row {
        case 0:
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: cellReuse,
                                                          for: indexPath)
            if let cell = cell as? GenericRecallCell {
                cell.recallLabel.text = "Stage 1"
            }
            return cell

        case 1:
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: cellReuse,
                                                          for: indexPath)
            if let cell = cell as? GenericRecallCell {
                cell.recallLabel.text = "Stage 2"

            }
            return cell
        case 2:
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: cellReuse,
                                                          for: indexPath)
            if let cell = cell as? GenericRecallCell {
                cell.recallLabel.text = "Stage 3"

            }
            return cell
        default:
            fatalError("This should not be happening")
        }
    }

}


extension RecallController: UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        switch indexPath.row {
        case 1:
            let StageOneController = StageController()
            navigationController?.pushViewController(StageOneController, animated: true)
        case 2:
            return
        default:
            return
        }
    }
}
