using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
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
    /// Interaction logic for AdvanceProvisioning.xaml
    /// </summary>
    public partial class AdvanceProvisioning : Page
    {
        private ICollectionView _ledgerView;
        public ObservableCollection<APEntry> APItems { get; set; }
        public ObservableCollection<string> EquipmentList { get; set; }

        private string _selectedEquipment= null;

        public AdvanceProvisioning()
        {
            InitializeComponent();
            LoadData();
            _ledgerView = CollectionViewSource.GetDefaultView(APItems);
            LedgerDataGrid.ItemsSource = _ledgerView;
            _ledgerView.Filter = CombinedFilter;
        }

        private void LoadData()
        {
            // Example: Replace with your real code to fetch data
            APItems = new()
            {
                new APEntry { DemandType = "Advanced Provision", EquipmentName = "Bolt", Quantity = "10" },
                new APEntry { DemandType = "Supply Demand", EquipmentName = "Nut", Quantity = "20" }
            };

            LedgerDataGrid.ItemsSource = APItems;
            EquipmentList = new ObservableCollection<string>(APItems.Select(a => a.EquipmentName).Distinct());
            Equipments.ItemsSource = EquipmentList;
        }

 

        private void Generate_Click(object sender, RoutedEventArgs e)
        {
            var popup = new Windows.GenerateNewAP();
            popup.Owner = Application.Current.MainWindow;
            popup.WindowStartupLocation = WindowStartupLocation.CenterOwner;
            bool? result = popup.ShowDialog();
            if (result == true)
            {
                // Refresh data after successful generation
                LoadData();
                _ledgerView.Refresh();
            }
        }

        private void Equipments_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }

        private void Analysis_Click(object sender, RoutedEventArgs e)
        {
            var mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new Views.AnalysisAP());
        }

        private void Report_Click(object sender, RoutedEventArgs e)
        {

        }

        private void APDemand_Checked(object sender, RoutedEventArgs e)
        {

        }

        private void SelectAllRadio_Checked(object sender, RoutedEventArgs e)
        {

        }

        private void SupplyDemand_Checked(object sender, RoutedEventArgs e)
        {

        }
    }

    public class APEntry
    {
        public string DemandNo { get; set; }
        public string EquipmentCode { get; set; }
        public string EquipmentName { get; set; }
        public string Quantity { get; set; }
        public string FinancialYear { get; set; }
        public string FullReceived { get; set; }
        public string PartialReceived { get; set; }
        public string Outstanding { get; set; }
        public string PercentageReceived { get; set; }
        public string DemandType { get; set; }
        public int IsSelected { get; set; }
    }



}
