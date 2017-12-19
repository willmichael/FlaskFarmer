//
//  AppDelegate.swift
//  FlaskRecall
//
//  Created by Michael Lee on 11/2/17.
//  Copyright © 2017 Michael Lee. All rights reserved.
//

import UIKit
import QuickLook

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?


    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        print("now we here")
        window = UIWindow(frame: UIScreen.main.bounds)

        let navigationBarApperance = UINavigationBar.appearance()
        navigationBarApperance.titleTextAttributes = [NSAttributedStringKey.foregroundColor: UIColor.red]
        navigationBarApperance.tintColor = .gray


        let tabBarController = UITabBarController()
        let tabViewController1 = MainViewController()
        let tabViewController2 = RecallController()
        let tabViewController3 = PreviewViewController()
        let rvController = UIViewController()

        let navigationController1 = UINavigationController(rootViewController: tabViewController1)
        let navigationController2 = UINavigationController(rootViewController: tabViewController2)
        let navigationController3 = UINavigationController(rootViewController: tabViewController3)
        let navRVController = UINavigationController(rootViewController: rvController)

//        let controllers = [tabViewController1, tabViewController2, tabViewController3, navRVController]
        let controllers = [navigationController1, navigationController2, navigationController3]

        tabBarController.viewControllers = controllers
        tabBarController.tabBar.tintColor = .red

        navigationController1.tabBarItem = UITabBarItem(title: "Beggining", image: #imageLiteral(resourceName: "icon_home_2x"), selectedImage: nil)
        navigationController2.tabBarItem = UITabBarItem(title: "Middle", image: #imageLiteral(resourceName: "icon_home_2x"), selectedImage: nil)
        navigationController3.tabBarItem = UITabBarItem(title: "End", image: #imageLiteral(resourceName: "icon_home_2x"), selectedImage: nil)
//        navigationController4.tabBarItem = UITabBarItem(title: "Account", image: #imageLiteral(resourceName: "icon_home_2x"), selectedImage: nil)

        window?.rootViewController = tabBarController
        window?.makeKeyAndVisible()
        return true
    }

    func application(_ app: UIApplication, open inputURL: URL, options: [UIApplicationOpenURLOptionsKey : Any] = [:]) -> Bool {
        print("we are here")
        guard inputURL.isFileURL
            else { return false }

        print("inputURL -> \(inputURL)")
        let previewController = PreviewViewController()
        previewController.fileURL = inputURL

        print("almost there")



        print("not here")

//        browserController.revealDocument(at: inputURL, importIfNeeded: true) {
//            (revealedDocumentURL, error) in
//            if let revealedDocumentURL = revealedDocumentURL {
//                present(documentURL: revealedDocumentURL)
//            } else if let error = error {
//                presentError(error)
//            }
//
//        }

        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }


}

