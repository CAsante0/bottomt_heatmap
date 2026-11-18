import argparse
import sys
from src import heatmap

def main():
    parser = argparse.ArgumentParser(
        description="Generate an average heatmap from a directory of daily NetCDF files."
    )
    
    parser.add_argument(
        "-i", "--input", "--mnt1",
        required=True, 
        help="Input directory containing daily .nc files"
    )
    parser.add_argument(
        "-o", "--output", "--mnt3", 
        required=True, 
        help="Output filepath for the image (e.g., output.png)"
    )
    parser.add_argument(
        "-v", "--var", 
        default="bottomT", 
        help="The target variable to average and plot (default: bottomT)"
    )    
    parser.add_argument(
        "-s", "--supplementary", "--mnt2",
        default=None, 
        help="Supplementary root directory for additional NetCDF files (optional)"
    )
    
    
    args = parser.parse_args()
    
    try:
        heatmap.generate_average_heatmap(args.input, args.output, args.var)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()