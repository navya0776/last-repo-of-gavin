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
    /// Interaction logic for Page1.xaml
    /// </summary>
    public partial class Dashboard : Page
    {
        public Dashboard()
        {
            InitializeComponent();
        }

        private bool isExpanded = false;

        //private void StoreButton_Click(object sender, RoutedEventArgs e)
        //{
        //    double targetHeight = isExpanded ? 0 : 90; // 3 menu buttons × 30 height each

        //    var animation = new System.Windows.Media.Animation.DoubleAnimation
        //    {
        //        To = targetHeight,
        //        Duration = TimeSpan.FromMilliseconds(300)
        //    };

        //    StoreMenu.BeginAnimation(Border.HeightProperty, animation);

        //    isExpanded = !isExpanded;
        //}

        //private void LedgerButton_Click(object sender, RoutedEventArgs e)
        //{
        //    var mainWindow = (MainWindow)Application.Current.MainWindow;
        //    mainWindow.MainFrame.Navigate(new Ledger());
        //}
        private void Provisioning_Click(object sender, RoutedEventArgs e)
        {
            var mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new AdvanceProvisioning());

        }
        //private void LedgerMaintenance_Click(object sender, RoutedEventArgs e)
        //{
        //    MessageBox.Show("Open Ledger & OS Page");
        //}
        //private void OverhaulScale_Click(object sender, RoutedEventArgs e)
        //{
        //    MessageBox.Show("Open Ledger & OS Page");
        //}
        //private void Receipt_Click(object sender, RoutedEventArgs e)
        //{
        //    MessageBox.Show("Open Ledger & OS Page");
        //}
        //private void Issue_Click(object sender, RoutedEventArgs e)
        //{
        //    MessageBox.Show("Open Ledger & OS Page");
        //}
        //private void Alert_Click(object sender, RoutedEventArgs e)
        //{
        //    MessageBox.Show("Open Ledger & OS Page");
        //}

        //private StackPanel currentlyExpandedMenu = null;

        //private void MainButton_Click(object sender, RoutedEventArgs e)
        //{
        //    StackPanel menuToShow = null;

        //    if (sender == StoreButton) menuToShow = StoreMenu;
        //    else if (sender == SalesButton) menuToShow = SalesMenu;

        //    // Collapse previously expanded menu
        //    if (currentlyExpandedMenu != null && currentlyExpandedMenu != menuToShow)
        //        currentlyExpandedMenu.Visibility = Visibility.Collapsed;

        //    // Toggle clicked menu
        //    if (menuToShow.Visibility == Visibility.Visible)
        //    {
        //        menuToShow.Visibility = Visibility.Collapsed;
        //        currentlyExpandedMenu = null;
        //    }
        //    else
        //    {
        //        menuToShow.Visibility = Visibility.Visible;
        //        currentlyExpandedMenu = menuToShow;
        //    }
        //}

        StackPanel currentPanel = null;
        Button currentButton = null;

        private void MainButton_Click(object sender, RoutedEventArgs e)
        {
            Button clickedButton = (Button)sender;
            StackPanel clickedPanel = (StackPanel)((clickedButton.Parent as StackPanel).Children[1]);

            // Collapse previously open menu
            if (currentPanel != null && currentPanel != clickedPanel)
            {
                currentPanel.Visibility = Visibility.Collapsed;
                currentButton.Visibility = Visibility.Visible;
            }

            // Toggle selected menu
            clickedButton.Visibility = Visibility.Collapsed;
            clickedPanel.Visibility = Visibility.Visible;

            currentPanel = clickedPanel;
            currentButton = clickedButton;
        }

        private void Ledger_click(object sender, RoutedEventArgs e)
        {
            var mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new Ledger());
        }

        private void Reciept_click(object sender, RoutedEventArgs e)
        {
            var mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new Ledger());
        }
    }

}
