using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using static IMS.SAPEAAviews.Challan;

namespace IMS.SAPEAAviews
{
    public partial class GFR : Page
    {
        public ObservableCollection<ChallanItem> GFRList { get; set; }

        private List<ChallanItem> _fullBackupList;
        private List<string> _columns;

        public GFR()
        {
            InitializeComponent();

            GFRList = new ObservableCollection<ChallanItem>();
            DataContext = GFRList;

            LoadData();
        }

        // ------------------------------------------------------------
        // LOAD GFR DATA (Replace placeholder API with correct one)
        // ------------------------------------------------------------
        private async void LoadData()
        {
            //try
            //{
            //    // Replace this API call later with correct endpoint
            //    var data = await ApiService.GetChallanListAsync();

            //    GFRList.Clear();
            //    foreach (var item in data)
            //        GFRList.Add(item);

            //    _fullBackupList = data.ToList();

            //    LoadColumnSelector();
            //    LoadGridColumns();
            //}
            //catch (Exception ex)
            //{
            //    MessageBox.Show("Failed to load GFR data:\n" + ex.Message,
            //                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            //}
        }

        // ------------------------------------------------------------
        // LOAD DYNAMIC COLUMNS
        // ------------------------------------------------------------
        private void LoadGridColumns()
        {
            JobsGrid.Columns.Clear();

            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Srl", Binding = new System.Windows.Data.Binding("Srl"), Width = 80 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "LPR No", Binding = new System.Windows.Data.Binding("Lpr_No"), Width = 120 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Date", Binding = new System.Windows.Data.Binding("Date"), Width = 120 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Indent No", Binding = new System.Windows.Data.Binding("Indent_No"), Width = 120 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Job No", Binding = new System.Windows.Data.Binding("Job_No_Comp_Dt"), Width = 160 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "OHS", Binding = new System.Windows.Data.Binding("Ohs"), Width = 100 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Page", Binding = new System.Windows.Data.Binding("Page"), Width = 80 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Part No", Binding = new System.Windows.Data.Binding("Part_No"), Width = 140 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Nomen", Binding = new System.Windows.Data.Binding("Nomen"), Width = 180 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Qty", Binding = new System.Windows.Data.Binding("Qty"), Width = 70 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Recd", Binding = new System.Windows.Data.Binding("Recd"), Width = 80 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "SO", Binding = new System.Windows.Data.Binding("So"), Width = 120 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "SO Date", Binding = new System.Windows.Data.Binding("So_Date"), Width = 120 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Vendor", Binding = new System.Windows.Data.Binding("Vend"), Width = 140 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Rate", Binding = new System.Windows.Data.Binding("Rate"), Width = 80 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Status", Binding = new System.Windows.Data.Binding("Status"), Width = 140 });
        }

        // ------------------------------------------------------------
        // POPULATE COLUMN SELECTOR
        // ------------------------------------------------------------
        private void LoadColumnSelector()
        {
            _columns = new List<string>
            {
                "Lpr_No",
                "Indent_No",
                "Part_No",
                "Nomen",
                "Vend",
                "Status"
            };

            ColumnSelector.ItemsSource = _columns;
            ColumnSelector.SelectedIndex = 0;
        }

        // ------------------------------------------------------------
        // SEARCH LOGIC
        // ------------------------------------------------------------
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_fullBackupList == null)
                return;

            string keyword = SearchBox.Text.Trim().ToLower();
            string column = ColumnSelector.SelectedItem?.ToString();

            if (string.IsNullOrWhiteSpace(keyword))
            {
                ResetList();
                return;
            }

            var filtered = _fullBackupList.Where(v =>
            {
                var prop = v.GetType().GetProperty(column)?.GetValue(v, null);
                if (prop == null) return false;
                return prop.ToString().ToLower().Contains(keyword);
            });

            GFRList.Clear();
            foreach (var item in filtered)
                GFRList.Add(item);
        }

        private void ResetList()
        {
            GFRList.Clear();
            foreach (var item in _fullBackupList)
                GFRList.Add(item);
        }

        // ------------------------------------------------------------
        // LAST X DAYS FILTER
        // ------------------------------------------------------------
        private void DaysFilterBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (_fullBackupList == null) return;

            string selection = (DaysFilterBox.SelectedItem as ComboBoxItem)?.Content.ToString();

            int days = selection switch
            {
                "Last 7 Days" => 7,
                "Last 15 Days" => 15,
                "Last 30 Days" => 30,
                "Last 90 Days" => 90,
                _ => 0
            };

            if (days == 0)
            {
                ResetList();
                return;
            }

            DateTime threshold = DateTime.Now.AddDays(-days);

            var filtered = _fullBackupList.Where(v => v.Date >= threshold);

            GFRList.Clear();
            foreach (var item in filtered)
                GFRList.Add(item);
        }

        // ------------------------------------------------------------
        // SO >> ALL
        // ------------------------------------------------------------
        private void SO_All_Click(object sender, RoutedEventArgs e)
        {
            ResetList();
        }

        // ------------------------------------------------------------
        // SO >> NO
        // ------------------------------------------------------------
        private void SO_No_Click(object sender, RoutedEventArgs e)
        {
            var filtered = _fullBackupList.Where(i => string.IsNullOrWhiteSpace(i.So));

            GFRList.Clear();
            foreach (var item in filtered)
                GFRList.Add(item);
        }

        // ------------------------------------------------------------
        // BACK BUTTON
        // ------------------------------------------------------------
        private void LogoButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
