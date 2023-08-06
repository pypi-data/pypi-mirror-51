from cwitools import params
from cwitools.reduction import trim

import argparse

def main():

    #Handle input with argparse
    parser = argparse.ArgumentParser(description="""
    Crop axes of a single data cube or multiple data cubes. There are two usage
    options. (1) Run directly on a single cube (e.g. cwi_crop -cube mycube.fits
    -wcrop 4100,4200 -xcrop 10,60 ) and (2) run using a CWITools parameter file,
    loading all input cubes of a certaintype (e.g. cwi_crop -params mytarget.param
    -cubetype icubes.fits -wcrop 4100,4200 -xcrop 10,60)
    """)
    parser.add_argument('-cube',
                        type=str,
                        help='Cube to be cropped (for working on a single cube).',
                        default=None
    )
    parser.add_argument('-params',
                        type=str,
                        help='CWITools parameter file (for working on a list of input cubes).',
                        default=None
    )
    parser.add_argument('-cubetype',
                        type=str,
                        help='The cube type to load (e.g. icubes.fits) if working with a parameter file.',
                        default=None

    )
    parser.add_argument('-wcrop',
                        type=str,
                        help="Wavelength range, in Angstrom, to crop to (syntax 'w0,w1') (Default:0,-1)",
                        default='0,-1'
    )
    parser.add_argument('-xcrop',
                        type=str,
                        help="Subrange of x-axis to crop to (syntax 'x0,x1') (Default:0,-1)",
                        default='0,-1'
    )
    parser.add_argument('-ycrop',
                        type=str,
                        help="Subrange of y-axis to crop to (syntax 'y0,y1') (Default:0,-1)",
                        default='0,-1'
    )
    parser.add_argument('-ext',
                        type=str,
                        help='The filename extension to add to cropped cubes. Default: .c.fits'
    )
    args = parser.parse_args()

    #Make list out of single cube if working in that mode
    if args.cube!=None and args.params==None and args.cubetype==None:

        if os.path.isfile(args.cube): fileList = [args.cube]
        else:
            raise FileNotFoundError("Input file not found. \nFile:%s"%args.cube)

    #Load list from parameter files if working in that mode
    elif args.cube==None and args.params!=None and args.cubetype!=None:

        # Check if any parameter values are missing (set to set-up mode if so)
        if os.path.isfile(ags.paramPath): params = params.loadparams(args.paramPath)
        else:
            raise FileNotFoundError("Parameter file not found.\nFile:%s"%args.paramPath)

        # Get filenames
        fileList = params.findfiles(params,cubeType)

    #Make sure usage is understood if some odd mix
    else:
        raise SyntaxError("""
        Usage should be one of the following modes:\
        \n\nUse -cube argument to specify one input cube to crop\
        \nOR\
        \nUse -params AND -cubetype flag together to load cubes from parameter file.
        """)

    try: x0,x1 = ( int(x) for x in args.xcrop.split(','))
    except:
        raise ValueError("Could not parse -xcrop, should be comma-separated integer tuple.")

    try: y0,y1 = ( int(y) for y in args.ycrop.split(','))
    except:
        raise ValueError("Could not parse -ycrop, should be comma-separated integer tuple.")

    try: w0,w1 = ( int(y) for w in args.wcrop.split(','))
    except:
        raise ValuError("Could not parse -wcrop, should be comma-separated integer tuple.")

    # Open fits objects
    for fileName in fileList:

        fitsFile = fits.open(fileName)

        # Pass to trimming function
        trimmedFits = trim(fitsFile,fileExt=args.ext,xcrop=(x0,x1),ycrop=(y0,y1),wcrop=(w0,w1))

        outFileName = fileName.replace('.fits',args.ext)
        trimmedFits.writeto(outFileName,overwrite=True)
        print("Saved %s"%outFileName)

if __name__=="__main__": main()
