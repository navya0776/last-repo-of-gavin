using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Input;

namespace IMS.Windows
{
    public partial class GenerateNewAP : Window
    {
        public List<EquipmentResponse> EquipmentList { get; set; }

        public GenerateNewAP()
        {
            InitializeComponent();

            // ViewModel holding DemandCreate
            DataContext = new GenerateApViewModel();

            // Load dropdown equipment list from backend
            LoadEquipments();
        }

        // LOAD EQUIPMENT LIST FROM /demand/equipments/
        public async void LoadEquipments()
        {
            try
            {
                var list = await ApiService.GetAllEquipmentsAsync();
                EquipmentList = list;

                cmbEquipment.ItemsSource = EquipmentList;
                cmbEquipment.DisplayMemberPath = "equipment_name";
                cmbEquipment.SelectedValuePath = "eqpt_code";
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to load equipments: " + ex.Message);
            }
        }

        private static readonly Regex _numRegex = new Regex("^[0-9]+$");
        private void Numeric_PreviewTextInput(object sender, TextCompositionEventArgs e)
            => e.Handled = !_numRegex.IsMatch(e.Text);

        // SUBMIT NEW DEMAND  → POST /demand/
        private async void Ok_Click(object sender, RoutedEventArgs e)
        {
            var vm = (GenerateApViewModel)DataContext;
            var model = vm.Model;

            // Fill fields from UI

            // 1. Equipment (code + name)
            if (cmbEquipment.SelectedItem is EquipmentResponse eq)
            {
                model.eqpt_code = eq.eqpt_code;
                model.eqpt_name = eq.equipment_name;
            }

            // 2. Fin year
            if (cmbFinYear.SelectedItem is System.Windows.Controls.ComboBoxItem fyItem)
            {
                model.fin_year = fyItem.Content?.ToString();
            }

            // 3. Demand type (APD / SPD)
            if (rbDemandTypeSPD.IsChecked == true)
                model.demand_type = "SPD";
            else
                model.demand_type = "APD";

            // 4. No of eqpt demand placed
            if (int.TryParse(txtNoEqptDemandPlaced.Text, out var placed))
                model.no_of_apd_demand_placed = placed;
            else
                model.no_of_apd_demand_placed = 0;

            // 5. Optional fields
            model.store_code = txtStore.Text.Trim();
            model.make = txtMake.Text.Trim();
            model.scale_or_ssg_ref = txtScaleRef.Text.Trim();
            model.demand_auth = txtDemandAuth.Text.Trim();
            model.remarks = txtRemarks.Text.Trim();

            // Validate
            if (!vm.IsValid())
            {
                MessageBox.Show("Please fill all required fields (equipment, fin year, demand type).");
                return;
            }

            try
            {
                await ApiService.CreateDemandAsync(model);

                MessageBox.Show("AP Demand created successfully!");
                this.DialogResult = true;   // inform caller (AdvanceProvisioning) to refresh
                this.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error creating demand:\n" + ex.Message);
            }
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
            => this.Close();

        private void Help_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Fill the fields and click OK to create a new AP demand.", "Help");

        private void LedgerPicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Ledger picker here (to be implemented).");

        private void ScalePicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Scale/Issue picker here (to be implemented).");

        private void AssyPicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Assy/Component picker here (to be implemented).");
    }
}
