//
//  SignPass2RegisterViewController.m
//  SignPass2
//
//  Created by Maneli Rabizadeh on 11/13/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import "SignPass2RegisterViewController.h"
#import "SignPass2SignatureViewController.h"

@interface SignPass2RegisterViewController ()

@end

@implementation SignPass2RegisterViewController

-(IBAction)Back:(id)sender
{
    [self dismissViewControllerAnimated:YES completion:NULL];
}
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}
-(IBAction)createSignature:(id)sender{
    SignPass2SignatureViewController *csp=[[SignPass2SignatureViewController alloc] initWithNibName:nil bundle:nil];
    [self presentModalViewController:csp animated:YES];
    
}
- (void)viewDidLoad
{
    [super viewDidLoad];
    usernameText.keyboardType=UIKeyboardTypeAlphabet;
    emailText.keyboardType=UIKeyboardTypeEmailAddress;
    // Do any additional setup after loading the view from its nib.
}
- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    [self.view endEditing:YES];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
