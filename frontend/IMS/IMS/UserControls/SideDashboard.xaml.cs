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

        private void ToggleSidebarButton_Click(object sender, RoutedEventArgs e)
        {
            if (isCollapsed)
            {
                // Expand sidebar
                SidebarColumn.Width = new GridLength(150);
                MenuButtons.Visibility = Visibility.Visible;
                ToggleSidebarButton.Content = "X";
                ToggleSidebarButton.HorizontalAlignment = HorizontalAlignment.Right;
            }
            else
            {
                // Collapse sidebar to top button only
                SidebarColumn.Width = new GridLength(30);
                MenuButtons.Visibility = Visibility.Collapsed;
                ToggleSidebarButton.Content = "☰";
                ToggleSidebarButton.HorizontalAlignment = HorizontalAlignment.Center;
                ToggleSidebarButton.Margin = new Thickness(0);
            }

            isCollapsed = !isCollapsed;
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
    }
}
