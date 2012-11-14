//
//  SignPass2LogInViewController.m
//  SignPass2
//
//  Created by Maneli Rabizadeh on 11/14/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import "SignPass2LogInViewController.h"

@interface SignPass2LogInViewController ()

@end

@implementation SignPass2LogInViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    usernameText.keyboardType=UIKeyboardTypeAlphabet;
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
-(IBAction)Done:(id)sender{
    [self.parentViewController dismissViewControllerAnimated:YES completion:nil];
    NSLog(@"test");
    
}
@end
