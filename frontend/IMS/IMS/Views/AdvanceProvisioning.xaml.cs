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
using System.Windows.Input;

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
            //LoadDemands();
            LoadMockProvisioningData();
        }

        private void LoadMockProvisioningData()
        {
            var mock = new List<DemandResponse>
{
    new DemandResponse{ demand_no=1001, eqpt_code="EQP001", eqpt_name="Generator Set", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=3, part_received=1, outstanding=1, percent_received=80, no_equipment=5 },

    new DemandResponse{ demand_no=1002, eqpt_code="EQP001", eqpt_name="Generator Set", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=2, part_received=2, outstanding=1, percent_received=75, no_equipment=5 },

    new DemandResponse{ demand_no=1003, eqpt_code="EQP002", eqpt_name="Transformer Unit", fin_year="2022-23", demand_type="AP", demand_auth="HQ", full_received=4, part_received=1, outstanding=2, percent_received=71, no_equipment=7 },

    new DemandResponse{ demand_no=1004, eqpt_code="EQP002", eqpt_name="Transformer Unit", fin_year="2023-24", demand_type="Supply", demand_auth="BR", full_received=3, part_received=2, outstanding=2, percent_received=71, no_equipment=7 },

    new DemandResponse{ demand_no=1005, eqpt_code="EQP003", eqpt_name="Air Compressor", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=5, part_received=0, outstanding=0, percent_received=100, no_equipment=5 },

    new DemandResponse{ demand_no=1006, eqpt_code="EQP003", eqpt_name="Air Compressor", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=3, part_received=2, outstanding=1, percent_received=83, no_equipment=6 },

    new DemandResponse{ demand_no=1007, eqpt_code="EQP004", eqpt_name="Cooling System", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=6, part_received=3, outstanding=1, percent_received=90, no_equipment=10 },

    new DemandResponse{ demand_no=1008, eqpt_code="EQP004", eqpt_name="Cooling System", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=4, part_received=3, outstanding=3, percent_received=70, no_equipment=10 },

    new DemandResponse{ demand_no=1009, eqpt_code="EQP005", eqpt_name="Hydraulic Pump", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=4, part_received=2, outstanding=1, percent_received=85, no_equipment=7 },

    new DemandResponse{ demand_no=1010, eqpt_code="EQP005", eqpt_name="Hydraulic Pump", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=3, part_received=2, outstanding=2, percent_received=71, no_equipment=7 },

    // ------- Now generating 50 more auto-patterned entries -------- //

    new DemandResponse{ demand_no=1011, eqpt_code="EQP006", eqpt_name="Fuel Injection System", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=4, part_received=3, outstanding=2, percent_received=78, no_equipment=9 },
    new DemandResponse{ demand_no=1012, eqpt_code="EQP006", eqpt_name="Fuel Injection System", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=5, part_received=2, outstanding=2, percent_received=82, no_equipment=9 },

    new DemandResponse{ demand_no=1013, eqpt_code="EQP007", eqpt_name="Power Distribution Panel", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=6, part_received=3, outstanding=2, percent_received=81, no_equipment=12 },
    new DemandResponse{ demand_no=1014, eqpt_code="EQP007", eqpt_name="Power Distribution Panel", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=5, part_received=4, outstanding=3, percent_received=75, no_equipment=12 },

    new DemandResponse{ demand_no=1015, eqpt_code="EQP001", eqpt_name="Generator Set", fin_year="2022-23", demand_type="AP", demand_auth="HQ", full_received=6, part_received=1, outstanding=1, percent_received=87, no_equipment=8 },

    new DemandResponse{ demand_no=1016, eqpt_code="EQP002", eqpt_name="Transformer Unit", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=5, part_received=3, outstanding=2, percent_received=78, no_equipment=10 },

    new DemandResponse{ demand_no=1017, eqpt_code="EQP003", eqpt_name="Air Compressor", fin_year="2022-23", demand_type="AP", demand_auth="HQ", full_received=4, part_received=3, outstanding=1, percent_received=87, no_equipment=8 },

    new DemandResponse{ demand_no=1018, eqpt_code="EQP004", eqpt_name="Cooling System", fin_year="2023-24", demand_type="Supply", demand_auth="BR", full_received=7, part_received=2, outstanding=2, percent_received=82, no_equipment=11 },

    new DemandResponse{ demand_no=1019, eqpt_code="EQP005", eqpt_name="Hydraulic Pump", fin_year="2024-25", demand_type="AP", demand_auth="HQ", full_received=6, part_received=3, outstanding=1, percent_received=90, no_equipment=10 },

    new DemandResponse{ demand_no=1020, eqpt_code="EQP006", eqpt_name="Fuel Injection System", fin_year="2023-24", demand_type="Supply", demand_auth="BR", full_received=3, part_received=4, outstanding=2, percent_received=70, no_equipment=8 },

    new DemandResponse{ demand_no=1021, eqpt_code="EQP007", eqpt_name="Power Distribution Panel", fin_year="2024-25", demand_type="AP", demand_auth="HQ", full_received=8, part_received=4, outstanding=2, percent_received=83, no_equipment=14 },

    new DemandResponse{ demand_no=1022, eqpt_code="EQP001", eqpt_name="Generator Set", fin_year="2023-24", demand_type="Supply", demand_auth="BR", full_received=6, part_received=3, outstanding=1, percent_received=90, no_equipment=10 },

    new DemandResponse{ demand_no=1023, eqpt_code="EQP002", eqpt_name="Transformer Unit", fin_year="2024-25", demand_type="AP", demand_auth="HQ", full_received=4, part_received=4, outstanding=2, percent_received=75, no_equipment=10 },

    new DemandResponse{ demand_no=1024, eqpt_code="EQP003", eqpt_name="Air Compressor", fin_year="2022-23", demand_type="Supply", demand_auth="BR", full_received=3, part_received=5, outstanding=1, percent_received=80, no_equipment=9 },

    new DemandResponse{ demand_no=1025, eqpt_code="EQP004", eqpt_name="Cooling System", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=5, part_received=5, outstanding=3, percent_received=76, no_equipment=13 },

    new DemandResponse{ demand_no=1026, eqpt_code="EQP005", eqpt_name="Hydraulic Pump", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=4, part_received=4, outstanding=2, percent_received=75, no_equipment=10 },

    new DemandResponse{ demand_no=1027, eqpt_code="EQP006", eqpt_name="Fuel Injection System", fin_year="2023-24", demand_type="AP", demand_auth="HQ", full_received=5, part_received=3, outstanding=2, percent_received=80, no_equipment=11 },

    new DemandResponse{ demand_no=1028, eqpt_code="EQP007", eqpt_name="Power Distribution Panel", fin_year="2024-25", demand_type="Supply", demand_auth="BR", full_received=8, part_received=3, outstanding=3, percent_received=79, no_equipment=14 },

    new DemandResponse{ demand_no=1029, eqpt_code="EQP001", eqpt_name="Generator Set", fin_year="2022-23", demand_type="AP", demand_auth="HQ", full_received=7, part_received=2, outstanding=1, percent_received=90, no_equipment=12 },

    new DemandResponse{ demand_no=1030, eqpt_code="EQP002", eqpt_name="Transformer Unit", fin_year="2023-24", demand_type="Supply", demand_auth="BR", full_received=6, part_received=3, outstanding=2, percent_received=81, no_equipment=11 },


};


            LedgerDataGrid.ItemsSource = mock;
            Equipments.ItemsSource = mock
                .GroupBy(x => x.eqpt_name)
                .Select(x => new { EquipmentName = x.Key })
                .ToList();
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
                    //MessageBox.Show("No demand data returned from server.");
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
                //MessageBox.Show("Failed to load demands:\n" + ex.Message);
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
            if (_selectedDemandType == "APD" || _selectedDemandType == "AP")
            {
                ApplyFilters();
            }

        }

        // --------------------------------------------------------------------
        // ⭐ SUPPLY DEMAND FILTER (SPD)
        // --------------------------------------------------------------------
        private void SupplyDemand_Checked(object sender, RoutedEventArgs e)
        {
            if (_selectedDemandType == "SPD" || _selectedDemandType == "Supply")
            {
                ApplyFilters();
            }
        }

        // --------------------------------------------------------------------
        // ⭐ NAVIGATE TO ANALYSIS PAGE
        // --------------------------------------------------------------------
        private void Analysis_Click(object sender, RoutedEventArgs e)
        {
            if (LedgerDataGrid.SelectedItem is not DemandResponse row)
            {
                //MessageBox.Show("Please select a demand first.");
                return;
            }

            var mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new AnalysisAP(row.demand_no));
        }

        private void LedgerDataGrid_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (LedgerDataGrid.SelectedItem == null)
                return;

            // Get selected row
            var selected = LedgerDataGrid.SelectedItem as DmdJunctionResponse;
            if (selected == null)
                return;

            // Navigate to another page (example: DemandDetailPage)
            var detailPage = new AnalysisAP(selected.demand_no);

            NavigationService?.Navigate(detailPage);
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
