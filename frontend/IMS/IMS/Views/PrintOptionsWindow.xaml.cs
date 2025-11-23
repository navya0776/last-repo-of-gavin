using System.Printing;
using System.Windows;
using System.Windows.Controls;

namespace IMS.Views
{
    public partial class PrintOptionsWindow : Window
    {
        public PageOrientation SelectedOrientation { get; set; } = PageOrientation.Portrait;
        public PageMediaSizeName SelectedPaperSize { get; set; } = PageMediaSizeName.ISOA4;

        public PrintOptionsWindow()
        {
            InitializeComponent();

            // Set defaults (A4 Portrait)
            OrientationCombo.SelectedIndex = 0; // Portrait
            PaperSizeCombo.SelectedIndex = 0;   // A4
            FitWidthCheck.IsChecked = true;
        }

        public PrintOptions GetOptions()
        {
            var opt = new PrintOptions
            {
                Orientation = SelectedOrientation,
                PaperSize = SelectedPaperSize,
                FitToWidth = FitWidthCheck.IsChecked == true,
                FitToHeight = FitHeightCheck.IsChecked == true
            };
            return opt;
        }

        private void Print_Click(object sender, RoutedEventArgs e)
        {
            // Orientation
            if (OrientationCombo.SelectedIndex == 0)
                SelectedOrientation = PageOrientation.Portrait;
            else
                SelectedOrientation = PageOrientation.Landscape;

            // Paper size
            switch ((PaperSizeCombo.SelectedItem as ComboBoxItem)?.Content?.ToString())
            {
                case "A3":
                    SelectedPaperSize = PageMediaSizeName.ISOA3;
                    break;
                case "Letter":
                    SelectedPaperSize = PageMediaSizeName.NorthAmericaLetter;
                    break;
                default:
                    SelectedPaperSize = PageMediaSizeName.ISOA4;
                    break;
            }

            DialogResult = true;
            Close();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}
