using System.Windows;
using System.Windows.Media;

namespace IMS
{
    public partial class MainWindow : Window
    {
        private bool isStoreExpanded = false;

        public MainWindow()
        {
            InitializeComponent();
            MainFrame.Navigate(new Views.Ledger());
        }

        private void Header_Loaded(object sender, RoutedEventArgs e)
        {

        }
    }
}
