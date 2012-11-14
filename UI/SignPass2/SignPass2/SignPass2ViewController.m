//
//  SignPass2ViewController.m
//  SignPass2
//
//  Created by Maneli Rabizadeh on 10/18/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import "SignPass2ViewController.h"

@interface SignPass2ViewController ()

@end

@implementation SignPass2ViewController

- (void)viewDidLoad
{
    myView.backgroundColor=[UIColor lightGrayColor];
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}
-(IBAction)ShowNextView:(id)sender{
    
    
    SignPass2RegisterViewController *nvc=[[SignPass2RegisterViewController alloc] initWithNibName:nil bundle:nil];
    [self presentModalViewController:nvc animated:YES];
    
}
-(IBAction)logInView:(id)sender{
    SignPass2LogInViewController *logView=[[SignPass2LogInViewController alloc] initWithNibName:nil bundle:nil];
    [self presentModalViewController:logView animated:YES];
}
@end
