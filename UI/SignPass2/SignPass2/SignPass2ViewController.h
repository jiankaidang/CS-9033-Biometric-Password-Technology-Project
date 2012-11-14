//
//  SignPass2ViewController.h
//  SignPass2
//
//  Created by Maneli Rabizadeh on 10/18/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SignPass2RegisterViewController.h"
#import "SignPass2LogInViewController.h"

@interface SignPass2ViewController : UIViewController
{
    IBOutlet UIView *myView;
    IBOutlet UILabel *welcomeLabel;
    IBOutlet UIButton *registerView;
    
}
@property (strong, nonatomic) UIWindow *myWindow;
//@property (nonatomic, readonly) UIViewController *MyView;
-(IBAction)ShowNextView:(id)sender;
-(IBAction)logInView:(id)sender;
-(void)presentModalViewController:(UIViewController *)modalViewController animated:(BOOL)animated;
-(void)dismissModalViewControllerAnimated:(BOOL)animated;
@end

