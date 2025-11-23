using System.Printing;

namespace IMS.Views
{
    public class PrintOptions
    {
        public PageOrientation Orientation { get; set; }
        public PageMediaSizeName PaperSize { get; set; }
        public bool FitToWidth { get; set; }
        public bool FitToHeight { get; set; }
    }
}
