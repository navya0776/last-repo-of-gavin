using IMS.Models;
using IMS.Services;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace IMS.Views
{
    public partial class CentralDemand : Page
    {
        public CentralDemand()
        {
            InitializeComponent();
            LoadMasterList();
        }

        private async void LoadMasterList()
        {
            try
            {
                var list = await ApiService.GetCDSAsync();
                MasterGrid.ItemsSource = list;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to load master list:\n" + ex.Message);
            }
        }

        private void AddEqpt_Click(object sender, RoutedEventArgs e)
        {
            ((MainWindow)Application.Current.MainWindow).MainFrame.Navigate(new AddEqpt());
        }

        private void JobMaster_Click(object sender, RoutedEventArgs e)
        {
            var selected = MasterGrid.SelectedItem as MasterListItem;

            if (selected == null)
            {
                MessageBox.Show("Select an equipment row first.");
                return;
            }

            ((MainWindow)Application.Current.MainWindow).MainFrame.Navigate(
                new JobMaster(selected.eqpt_code)
            );
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            ((MainWindow)Application.Current.MainWindow).MainFrame.Navigate(new Dashboard());
        }

        private void MasterGrid_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            var selected = MasterGrid.SelectedItem as MasterListItem;

            if (selected == null)
            {
                MessageBox.Show("Please select a row.");
                return;
            }

            // Navigate and pass eqpt_code
            ((MainWindow)Application.Current.MainWindow).MainFrame.Navigate(
                new CentralDemandNavigationPage(selected.eqpt_code)
            );
        }

    }
}
