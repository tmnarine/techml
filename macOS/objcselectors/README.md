# Working around the 2 parameter limit when calling an Objective-C selector

In Objective-C, selectors are defined in the following way:

    SEL sel = @selector(pushData);

@ is Objective-C's way of saying what follows is special.  In this example, the string "pushData" will be the name of the method you wish to find on an object.

An implementation/class can be queried to check if the selector exists:

    BOOL responds = [object respondsToSelector:sel];

To call the implementation method use:

    [object performSelector:];

There are 3 different methods for calling a selector:

    performSelector:
    performSelector:withObject:
    performSelector:withObject:withObject:

See [NSObject](https://developer.apple.com/documentation/objectivec/1418956-nsobject) for more information.

At most 2 parameters are allowed when calling a selector.  A possible workaround for this issue is to use an array of NS types as shown below.

An example of the calling code:

    -(VOID) pushSomeData(NSObject object, NSUInteger N, NSUInter H, NSUInter W)
    {
        static SEL sel = nil;
        static BOOL responds = false;

        if (sel == nil)
        {
            sel = @selector(pushData);
            responds = [object respondsToSelector: sel];
        }

        if (responds)
        {
            id parameters[] =
            {
                @"NSUInteger-N", [NSNumber numberWithUnsignedInteger: N],
                @"NSUInteger-H", [NSNumber numberWithUnsignedInteger: H],
                @"NSUInteger-W", [NSNumber numberWithUnsignedInteger: W]
            };
            NSUInteger count = sizeof(parameters)/sizeof(id);
            NSArray *parameterList = [NSArray arrayWithObjects: parameters count: count];
            [object performSelector: sel withObject: parameterList];
            [parameterList dealloc];
        }
        else
        {
            NSLog(@"Selector not found");
        }
    }

The responding code could be implemented as:

    -(VOID) pushData: (NSArray*) parameterList
    {
        if (parameterList == nil)
        {
            return;
        }

        NSUInteger index = NSNotFound;

        index =  [parameterList indexOfObject: @"NSUInteger-N"];
        NSUInteger N = (index == NSNotFound) ? 0 : [(NSNumber*) parameterList(index+1) unsignedIntegerValue];

        index =  [parameterList indexOfObject: @"NSUInteger-H"];
        NSUInteger H = (index == NSNotFound) ? 0 : [(NSNumber*) parameterList(index+1) unsignedIntegerValue];

        index =  [parameterList indexOfObject: @"NSUInteger-W"];
        NSUInteger W = (index == NSNotFound) ? 0 : [(NSNumber*) parameterList(index+1) unsignedIntegerValue];
    }
