using IMS.Models;
using IMS.Services;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;

namespace IMS.Views
{
    public partial class AddEqpt : Page
    {
        private List<MasterListItem> masterList;

        public AddEqpt()
        {
            InitializeComponent();
            LoadMasterTable();
        }

        private async void LoadMasterTable()
        {
            try
            {
                masterList = await ApiService.GetMasterListAsync();

                EquipmentDataGrid.ItemsSource = masterList;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to load master list:\n" + ex.Message);
            }
        }

        private void EquipmentDataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (EquipmentDataGrid.SelectedItem is MasterListItem item)
            {
                // Auto-fill fields based on row clicked
                DatabaseTextBox.Text = item.eqpt_code;
                LedgerTextBox.Text = item.ledger_code;
            }
        }

        private async void save_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(EquipmentNameTextBox.Text))
            {
                MessageBox.Show("Enter equipment name.");
                return;
            }
            if (string.IsNullOrWhiteSpace(GroupTextBox.Text))
            {
                MessageBox.Show("Enter group.");
                return;
            }
            if (string.IsNullOrWhiteSpace(DatabaseTextBox.Text) || string.IsNullOrWhiteSpace(LedgerTextBox.Text))
            {
                MessageBox.Show("Select a row from the list.");
                return;
            }

            var payload = new AddEquipmentPayload
            {
                equipment_name = EquipmentNameTextBox.Text,
                eqpt_code = DatabaseTextBox.Text,
                ledger_code = LedgerTextBox.Text,
                grp = GroupTextBox.Text
            };

            bool ok = await ApiService.AddEquipmentAsync(payload);

            if (ok)
            {
                MessageBox.Show("Equipment added successfully!");

                // Navigate back to CentralDemand
                ((MainWindow)Application.Current.MainWindow).MainFrame.Navigate(
                    new CentralDemand()
                );
            }
            else
            {
                MessageBox.Show("Failed to add equipment.");
            }
        }

        private void cancel_Click(object sender, RoutedEventArgs e)
        {
            ((MainWindow)Application.Current.MainWindow).MainFrame.GoBack();
        }
    }
}
