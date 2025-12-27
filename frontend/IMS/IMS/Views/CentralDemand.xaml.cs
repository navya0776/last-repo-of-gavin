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

        private static Random R = new Random();

        private async void LoadMasterList()
        {
            try
            {
                // Instead of calling backend:
                // var list = await ApiService.GetCDSAsync();
                // MasterGrid.ItemsSource = list;

                MasterGrid.ItemsSource = GenerateMockMasterList(120); // generate 120 rows
            }
            catch (Exception ex)
            {
                //MessageBox.Show("Failed to load master list:\n" + ex.Message);
            }
        }
        private List<MasterListItem> GenerateMockMasterList(int count)
        {
            string[] ledgerHeads =
            {
        "Electrical", "Mechanical", "Instrumentation", "Power",
        "Cooling", "Hydraulics", "Safety", "Precision", "Fabrication"
    };

            string[] equipmentNames =
            {
        "Generator",
        "Air Compressor",
        "Cooling Assembly",
        "Power Regulator",
        "Sensor Array",
        "Valve Pack",
        "Hydraulic Pump",
        "Ignition Panel",
        "Control Unit",
        "Stabilizer",
        "Transmission Set"
    };

            var list = new List<MasterListItem>();

            for (int i = 1; i <= count; i++)
            {
                string eqCode = $"EQP-{R.Next(100, 999)}";
                string ledgerCode = $"LCD-{R.Next(1000, 9999)}";
                string nameBase = equipmentNames[R.Next(equipmentNames.Length)];

                list.Add(new MasterListItem
                {
                    ledger_code = ledgerCode,
                    eqpt_code = eqCode,
                    ledger_name = $"{nameBase} Master {R.Next(1, 50)}",
                    head = ledgerHeads[R.Next(ledgerHeads.Length)]
                });
            }

            return list;
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
