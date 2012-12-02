//
//  SignPass2LogInViewController.h
//  SignPass2
//
//  Created by Maneli Rabizadeh on 11/14/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface SignPass2LogInViewController : UIViewController
{
    IBOutlet UITextField *usernameText;
    __weak IBOutlet UIButton *verifySignature;
}
- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event;
-(IBAction)Done:(id)sender;
-(void)presentModalViewController:(UIViewController *)modalViewController animated:(BOOL)animated;
-(void)dismissModalViewControllerAnimated:(BOOL)animated;
- (IBAction)verifySignatureAction;
@end
