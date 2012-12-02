//
//  SignPass2SignatureViewController.h
//  SignPass2
//
//  Created by Jiankai Dang on 12/2/12.
//  Copyright (c) 2012 Maneli Kadkhodazadeh. All rights reserved.
//

#import <UIKit/UIKit.h>
@class PaintingWindow;
@class PaintingView;
@interface SignPass2SignatureViewController : UIViewController
@property (weak, nonatomic) IBOutlet PaintingView *drawingView;
@property CFTimeInterval		lastTime;
@end
