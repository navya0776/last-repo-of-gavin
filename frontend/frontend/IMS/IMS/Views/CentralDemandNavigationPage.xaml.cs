using IMS.Models;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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
    /// Interaction logic for CentralDemandNavigationPage.xaml
    /// </summary>
    public partial class CentralDemandNavigationPage : Page
    {
        public CentralDemandNavigationPage()
        {
            InitializeComponent();
            ObservableCollection<IMS.Models.CDS> _activeCDS = new();

        }

        private void DataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            MainWindow main = (MainWindow)Application.Current.MainWindow;
        }

        private void GenerateCSV_click(object sender, RoutedEventArgs e)
        {
            var mainWindow = Application.Current.MainWindow as MainWindow;
            mainWindow.MainFrame.Navigate(new Views.GenerateCRV());

        }
    }
}
