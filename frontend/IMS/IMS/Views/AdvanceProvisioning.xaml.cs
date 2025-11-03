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

        private bool CombinedFilter(object entry)
        {
            var row = entry as APEntry;
            if (row == null) return false;
            // Filter by Equipment
            if (!string.IsNullOrEmpty(_selectedEquipment) && row.EquipmentName != _selectedEquipment)
                return false;
            // Filter by Demand Type
            string selected = (FilterCombo.SelectedItem as ComboBoxItem).Content.ToString();
            if (selected != "All" && row.DemandType != selected)
                return false;
            return true;
        }

        private void ApplyFilter()
        {
            if (_ledgerView == null) return;

            string selected = (FilterCombo.SelectedItem as ComboBoxItem).Content.ToString();

            _ledgerView.Filter = entry =>
            {
                var row = entry as APEntry;
                if (row == null) return false;

                if (selected == "All")
                    return true;

                return row.DemandType == selected;
            };

            _ledgerView.Refresh();
        }

        private void FilterCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void Generate_Click(object sender, RoutedEventArgs e)
        {
            FormOverlay.Visibility = Visibility.Visible;
        }

        private void Equipments_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }

        private void Analysis_Click(object sender, RoutedEventArgs e)
        {
            var mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.MainFrame.Navigate(new Views.AnalysisAP());
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
