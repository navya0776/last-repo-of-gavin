using IMS.Services;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using static IMS.Models.DemandModel;

namespace IMS.Windows
{
    public partial class GenerateNewAP : Window
    {
        public List<LedgerResponse> EquipmentList { get; set; }

        public GenerateNewAP()
        {
            InitializeComponent();
            DataContext = new GenerateApViewModel();

            // Load dropdown equipment list
            LoadEquipments();
        }

        // FIX: Load equipment list from backend
        public async void LoadEquipments()
        {
            try
            {
                var list = await ApiService.GetAsync<List<LedgerResponse>>("/demand/equipments/");
                EquipmentList = list;

                cmbEquipment.ItemsSource = EquipmentList;
                cmbEquipment.DisplayMemberPath = "eqpt_name";
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

        // ⭐ OK CLICK → SUBMIT FORM TO BACKEND
        private async void Ok_Click(object sender, RoutedEventArgs e)
        {
            var vm = (GenerateApViewModel)DataContext;

            // Validate model before submitting
            if (!vm.IsValid())
            {
                MessageBox.Show("Please fill required fields.");
                return;
            }

            try
            {
                // IMPORTANT: specify generic type
                await ApiService.PostAsync<object>("/demand/", vm.Model);

                MessageBox.Show("AP Demand Created Successfully!");
                this.DialogResult = true;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error creating demand:\n" + ex.Message);
            }
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
            => this.Close();

        private void Help_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Fill the form and press Ok to generate AP demand.", "Help");

        private void LedgerPicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Ledger Name picker here.");

        private void ScalePicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Scale/Issue picker here.");

        private void AssyPicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Assy/Component picker here.");
    }
}
