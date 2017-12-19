//
//  GenericRecallCell.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/22/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit

class GenericRecallCell: UICollectionViewCell {

    let recallLabel = UILabel()

    override init(frame: CGRect) {
        super.init(frame: frame)

        recallLabel.text = "PlaceHolder"
        recallLabel.textColor = .black
        recallLabel.textAlignment = .center
        recallLabel.font = UIFont.systemFont(ofSize: 32)


        contentView.addSubview(recallLabel)
        contentView.backgroundColor = .white
        contentView.clipsToBounds = true
    }

    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func layoutSubviews() {
        recallLabel.frame = contentView.layoutMarginsGuide.layoutFrame
    }
}
