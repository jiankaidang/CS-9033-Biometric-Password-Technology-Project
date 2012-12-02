//
//  SignPass2RegisterViewController.h
//  SignPass2
//
//  Created by Maneli Rabizadeh on 11/13/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface SignPass2RegisterViewController : UIViewController
{
    IBOutlet UILabel *username;
    IBOutlet UILabel *email;
    IBOutlet UITextField *usernameText;
    IBOutlet UITextField *emailText;
    IBOutlet UIButton *createSignatureButton;
    
    
}
- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event;
-(IBAction)Back:(id)sender;
-(IBAction)createSignature:(id)sender;
-(void)presentModalViewController:(UIViewController *)modalViewController animated:(BOOL)animated;
-(void)dismissModalViewControllerAnimated:(BOOL)animated;
@end
