using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace IMS.Views
{
    /// <summary>
    /// Interaction logic for GenerateCRV.xaml
    /// </summary>
    public partial class GenerateCRV : Page
    {
        public GenerateCRV()
        {
            InitializeComponent();
        }

        private void PrintCRV_click(object sender, RoutedEventArgs e)
        {
            MainWindow mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new PrintCRV());
        }
    }
}
