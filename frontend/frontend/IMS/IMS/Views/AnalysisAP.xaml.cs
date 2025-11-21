using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using static IMS.Models.DemandModel;

namespace IMS.Views
{
    public partial class AnalysisAP : Page
    {
        private int _demandNo;

        public AnalysisAP(int demandNo)
        {
            InitializeComponent();
            _demandNo = demandNo;

            LoadDemandDetails();
        }

        // --------------------------------------------------
        // ⭐ LOAD ALL JUNCTION DETAILS FOR THIS DEMAND
        // Route hit: GET /demand/detail/{demand_no}
        // --------------------------------------------------
        private async void LoadDemandDetails()
        {
            try
            {
                var result = await ApiService.GetAsync<List<DmdJunctionResponse>>(
                    $"/demand/detail/{_demandNo}"
                );

                if (result != null)
                    LedgerDataGrid.ItemsSource = result;
                else
                    MessageBox.Show("No data returned from server.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading demand details:\n" + ex.Message);
            }
        }

        // --------------------------------------------------
        // ⭐ LOCK DEMAND
        // Route hit: POST /demand/{demand_no}/lock
        // --------------------------------------------------
        private async void LockDemand_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                await ApiService.PostAsync<object>(
                    $"/demand/{_demandNo}/lock", new { }
                );

                MessageBox.Show("Demand locked successfully.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unable to lock demand:\n" + ex.Message);
            }
        }

        // --------------------------------------------------
        // ⭐ UNLOCK DEMAND
        // Route hit: POST /demand/{demand_no}/unlock
        // --------------------------------------------------
        private async void UnlockDemand_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                await ApiService.PostAsync<object>(
                    $"/demand/{_demandNo}/unlock", new { }
                );

                MessageBox.Show("Demand unlocked.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unable to unlock demand:\n" + ex.Message);
            }
        }

        // --------------------------------------------------
        // ⭐ DELETE THE ENTIRE DEMAND
        // Route hit: DELETE /demand/{demand_no}
        // --------------------------------------------------
        private async void DeleteDemand_Click(object sender, RoutedEventArgs e)
        {
            var confirm = MessageBox.Show(
                "Are you sure you want to delete this demand?",
                "Confirm Delete",
                MessageBoxButton.YesNo,
                MessageBoxImage.Warning
            );

            if (confirm == MessageBoxResult.No)
                return;

            try
            {
                await ApiService.DeleteAsync($"/demand/{_demandNo}");
                MessageBox.Show("Demand deleted.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Unable to delete demand:\n" + ex.Message);
            }
        }

        private void LedgerDataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // Optional — You can show details about selected row here
        }
    }
}
