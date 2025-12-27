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

namespace IMS.UserControls
{
    public partial class SideDashboard : UserControl
    {
        private bool isCollapsed = false;

        public SideDashboard()
        {
            InitializeComponent();
        }

        private void ledger_Click(object sender, RoutedEventArgs e)
        {
            var mainWindow = Application.Current.MainWindow as MainWindow;
            mainWindow.MainFrame.Navigate(new Views.Ledger());
        }

        private void APprovisioning_Click(object sender, RoutedEventArgs e)
        {
            var mainWindow = Application.Current.MainWindow as MainWindow;
            mainWindow.MainFrame.Navigate(new Views.AdvanceProvisioning());
        }

        private void CDS_Click(object sender, RoutedEventArgs e)
        {
            var mainWindow = Application.Current.MainWindow as MainWindow;
            mainWindow.MainFrame.Navigate(new Views.CentralDemand());
        }
    }
}
