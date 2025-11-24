using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace IMS.Views
{
    public partial class AdvanceProvisioning : Page
    {
        private ICollectionView _view;

        public ObservableCollection<DemandResponse> DemandList { get; set; }
        public ObservableCollection<string> EquipmentList { get; set; }

        // Active filters
        private string _selectedEquipment = null;      // e.g. "Engine", "Pump"
        private string _selectedDemandType = null;     // "APD", "SPD", or null

        public AdvanceProvisioning()
        {
            InitializeComponent();
            LoadDemands();
        }

        // --------------------------------------------------------------------
        // ⭐ LOAD ALL DEMANDS FROM BACKEND
        // Route: GET /demand/
        // --------------------------------------------------------------------
        private async void LoadDemands()
        {
            try
            {
                var data = await ApiService.GetAsync<List<DemandResponse>>("/demand/");

                if (data == null)
                {
                    MessageBox.Show("No demand data returned from server.");
                    return;
                }

                DemandList = new ObservableCollection<DemandResponse>(data);

                _view = CollectionViewSource.GetDefaultView(DemandList);
                LedgerDataGrid.ItemsSource = _view;

                EquipmentList = new ObservableCollection<string>(
                    data.Select(x => x.eqpt_name).Distinct()
                );

                Equipments.ItemsSource = EquipmentList;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to load demands:\n" + ex.Message);
            }
        }

        // --------------------------------------------------------------------
        // ⭐ APPLY ALL ACTIVE FILTERS (TYPE + EQUIPMENT)
        // --------------------------------------------------------------------
        private void ApplyFilters()
        {
            if (_view == null) return;

            _view.Filter = item =>
            {
                var row = item as DemandResponse;

                bool equipmentMatch =
                    _selectedEquipment == null || row.eqpt_name == _selectedEquipment;

                bool typeMatch =
                    _selectedDemandType == null || row.demand_type == _selectedDemandType;

                return equipmentMatch && typeMatch;
            };
        }

        // --------------------------------------------------------------------
        // ⭐ EQUIPMENT FILTER (ListBox)
        // --------------------------------------------------------------------
        private void Equipments_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            _selectedEquipment = Equipments.SelectedItem as string;
            ApplyFilters();
        }

        // --------------------------------------------------------------------
        // ⭐ SELECT ALL (clears only demand type filter)
        // --------------------------------------------------------------------
        private void SelectAllRadio_Checked(object sender, RoutedEventArgs e)
        {
            _selectedDemandType = null;
            ApplyFilters();
        }

        // --------------------------------------------------------------------
        // ⭐ AP DEMAND FILTER (APD)
        // --------------------------------------------------------------------
        private void APDemand_Checked(object sender, RoutedEventArgs e)
        {
            _selectedDemandType = "APD";
            ApplyFilters();
        }

        // --------------------------------------------------------------------
        // ⭐ SUPPLY DEMAND FILTER (SPD)
        // --------------------------------------------------------------------
        private void SupplyDemand_Checked(object sender, RoutedEventArgs e)
        {
            _selectedDemandType = "SPD";
            ApplyFilters();
        }

        // --------------------------------------------------------------------
        // ⭐ NAVIGATE TO ANALYSIS PAGE
        // --------------------------------------------------------------------
        private void Analysis_Click(object sender, RoutedEventArgs e)
        {
            if (LedgerDataGrid.SelectedItem is not DemandResponse row)
            {
                MessageBox.Show("Please select a demand first.");
                return;
            }

            var mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new AnalysisAP(row.demand_no));
        }

        // --------------------------------------------------------------------
        // ⭐ GENERATE NEW AP DEMAND POPUP
        // --------------------------------------------------------------------
        private void Generate_Click(object sender, RoutedEventArgs e)
        {
            var popup = new Windows.GenerateNewAP();
            popup.Owner = Application.Current.MainWindow;

            if (popup.ShowDialog() == true)
            {
                LoadDemands(); // refresh grid after creating
            }
        }

        // Unused handlers kept to avoid warnings
        private void Report_Click(object sender, RoutedEventArgs e) { }
    }
}
