//
//  SignPass2SignatureViewController.m
//  SignPass2
//
//  Created by Jiankai Dang on 12/2/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import "SignPass2SignatureViewController.h"
#import "PaintingView.h"

//CONSTANTS:
#define kPaletteHeight			30
#define kPaletteSize			5
#define kMinEraseInterval		0.5

// Padding for margins
#define kLeftMargin				10.0
#define kTopMargin				10.0
#define kRightMargin			10.0
@interface SignPass2SignatureViewController ()

@end

@implementation SignPass2SignatureViewController
@synthesize drawingView;
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
    // Do any additional setup after loading the view from its nib.
    CGFloat					components[3];
    
	// Defer to the OpenGL view to set the brush color
	[drawingView setBrushColorWithRed:components[0] green:components[1] blue:components[2]];
    [drawingView setBackgroundColor:[UIColor whiteColor]];
    
    CGRect frame = CGRectMake(10.0, 10.0, 30, 115);
    UIButton *button = [[UIButton alloc] initWithFrame:frame];
    
    button.contentVerticalAlignment = UIControlContentVerticalAlignmentCenter;
    button.contentHorizontalAlignment = UIControlContentHorizontalAlignmentCenter;
    
    [button setTitle:@"HAha" forState:UIControlStateNormal];
    [button setTitleColor:[UIColor blackColor] forState:UIControlStateNormal];
    
    UIImage *buttonBackground = [UIImage imageNamed:@"VB.png"];
    UIImage *buttonBackgroundPressed = [UIImage imageNamed:@"VBP.png"];
    
    UIImage *newImage = [buttonBackground stretchableImageWithLeftCapWidth:12.0 topCapHeight:0.0];
    [button setBackgroundImage:newImage forState:UIControlStateNormal];
    
    UIImage *newPressedImage = [buttonBackgroundPressed stretchableImageWithLeftCapWidth:12.0 topCapHeight:0.0];
    [button setBackgroundImage:newPressedImage forState:UIControlStateHighlighted];
    
    // in case the parent view draws with a custom color or gradient, use a transparent color
    button.backgroundColor = [UIColor clearColor];
    [button addTarget:self action:@selector(collectSignatureArray:)forControlEvents:UIControlEventTouchUpInside];
    
    
    CGRect frameErase = CGRectMake(10.0, 355.0, 30, 115);
    UIButton *buttonErase = [[UIButton alloc] initWithFrame:frameErase];
    
    buttonErase.contentVerticalAlignment = UIControlContentVerticalAlignmentCenter;
    buttonErase.contentHorizontalAlignment = UIControlContentHorizontalAlignmentCenter;
    
    [buttonErase setTitle:@"HAha" forState:UIControlStateNormal];
    [buttonErase setTitleColor:[UIColor blackColor] forState:UIControlStateNormal];
    
    UIImage *buttonBackgroundErase = [UIImage imageNamed:@"EB.png"];
    UIImage *buttonBackgroundPressedErase = [UIImage imageNamed:@"EBP.png"];
    
    UIImage *newImageErase = [buttonBackgroundErase stretchableImageWithLeftCapWidth:12.0 topCapHeight:0.0];
    [buttonErase setBackgroundImage:newImageErase forState:UIControlStateNormal];
    
    UIImage *newPressedImageErase = [buttonBackgroundPressedErase stretchableImageWithLeftCapWidth:12.0 topCapHeight:0.0];
    [buttonErase setBackgroundImage:newPressedImageErase forState:UIControlStateHighlighted];
    
    // in case the parent view draws with a custom color or gradient, use a transparent color
    buttonErase.backgroundColor = [UIColor clearColor];
    [buttonErase addTarget:self action:@selector(eraseView:)forControlEvents:UIControlEventTouchUpInside];
    
    [drawingView addSubview:button];
    [drawingView addSubview:buttonErase];
    
    //    //[myButton addTarget:self action:@selector(goBackButtonClicked:)forControlEvents:UIControlEventTouchUpInside];
    // Look in the Info.plist file and you'll see the status bar is hidden
	// Set the style to black so it matches the background of the application
    UIApplication *application=[UIApplication sharedApplication];
	[application setStatusBarStyle:UIStatusBarStyleBlackTranslucent animated:NO];
	// Now show the status bar, but animate to the style.
	[application setStatusBarHidden:YES withAnimation:NO];
}
- (void)collectSignatureArray:(id)sender
{
    //NSLog(@"Call collect signature Array");
	[drawingView collectSignatureArrayFromView];
}


-(void) eraseView:(id)sender
{
	[drawingView erase];
}
@end
