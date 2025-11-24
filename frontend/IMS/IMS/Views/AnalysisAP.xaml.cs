using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;

namespace IMS.Views
{
    public partial class AnalysisAP : Page
    {
        private readonly int _demandNo;
        private bool _isLocked = false;


        public AnalysisAP(int demandNo)
        {
            InitializeComponent();
            _demandNo = demandNo;

            LoadDemandDetails();
        }

        // ---------------------------
        // LOAD JUNCTION DETAILS
        // ---------------------------
        private async void LoadDemandDetails()
        {
            var rows = await ApiService.GetAsync<List<DmdJunctionResponse>>($"demand/detail/{_demandNo}");

            LedgerDataGrid.ItemsSource = rows;

            // set initial lock state from backend
            if (rows.Count > 0)
                _isLocked = rows[0].is_locked;

            LockButton.Content = _isLocked ? "Unlock Demand" : "Lock Demand";
        }


        // ---------------------------
        // LOCK DEMAND
        // ---------------------------
        private async void LockDemand_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                await ApiService.PostAsync<object>($"demand/{_demandNo}/lock", new { });
                MessageBox.Show("Demand locked.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unable to lock demand:\n" + ex.Message);
            }
        }

        // ---------------------------
        // UNLOCK DEMAND
        // ---------------------------
        private async void UnlockDemand_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                await ApiService.PostAsync<object>($"demand/{_demandNo}/unlock", new { });
                MessageBox.Show("Demand unlocked.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unable to unlock demand:\n" + ex.Message);
            }
        }

        // ---------------------------
        // DELETE DEMAND
        // ---------------------------
        private async void DeleteDemand_Click(object sender, RoutedEventArgs e)
        {
            var confirm = MessageBox.Show(
                "Are you sure you want to delete this demand?",
                "Confirm Delete",
                MessageBoxButton.YesNo,
                MessageBoxImage.Warning
            );

            if (confirm != MessageBoxResult.Yes)
                return;

            try
            {
                await ApiService.DeleteAsync($"demand/{_demandNo}");
                MessageBox.Show("Demand deleted.");

                // Navigate back to AP list automatically
                var main = (MainWindow)Application.Current.MainWindow;
                main.MainFrame.Navigate(new AdvanceProvisioning());
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unable to delete demand:\n" + ex.Message);
            }
        }

        private async void ToggleLock_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_isLocked == false)
                {
                    // Lock demand
                    await ApiService.PostAsync<object>($"demand/{_demandNo}/lock", new { });
                    _isLocked = true;

                    MessageBox.Show("Demand locked.");
                    (sender as Button).Content = "Unlock Demand"; // change button label
                }
                else
                {
                    // Unlock demand
                    await ApiService.PostAsync<object>($"demand/{_demandNo}/unlock", new { });
                    _isLocked = false;

                    MessageBox.Show("Demand unlocked.");
                    (sender as Button).Content = "Lock Demand"; // change button label
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unable to change lock state:\n" + ex.Message);
            }
        }


        private void LedgerDataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // You can display selected row info here (optional)
        }
    }
}
