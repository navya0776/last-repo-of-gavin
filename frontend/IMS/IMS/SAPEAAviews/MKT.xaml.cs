using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace IMS.SAPEAAviews
{
    public partial class MKT : Page
    {
        public ObservableCollection<ShortOrderItem> Orders { get; set; }

        private List<ShortOrderItem> _backupList;
        private List<string> _columns;

        public MKT()
        {
            InitializeComponent();

            Orders = new ObservableCollection<ShortOrderItem>();
            DataContext = Orders;

            LoadData();
        }

        // ---------------------------------------------------------
        // LOAD DATA FROM BACKEND
        // ---------------------------------------------------------
        private async void LoadData()
        {
            //try
            //{
            //    var data = await ApiService.GetMKTAsync();   //  CALL YOUR MKT API HERE

            //    Orders.Clear();
            //    foreach (var d in data)
            //        Orders.Add(d);

            //    _backupList = data.ToList();   // For searching & filtering

            //    LoadColumnSelector();
            //    GenerateDynamicColumns();
            //}
            //catch (Exception ex)
            //{
            //    MessageBox.Show("Failed to load MKT data:\n" + ex.Message,
            //                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            //}
        }

        // ---------------------------------------------------------
        // BUILD COLUMNS DROPDOWN
        // ---------------------------------------------------------
        private void LoadColumnSelector()
        {
            _columns = new List<string>
            {
                "Srl",
                "Part_No",
                "Nomen",
                "Qty",
                "Vend",
                "Status",
                "So",
                "Date"
            };

            ColumnSelector.ItemsSource = _columns;
            ColumnSelector.SelectedIndex = 0;
        }

        // ---------------------------------------------------------
        // DYNAMIC DATA GRID COLUMNS
        // ---------------------------------------------------------
        private void GenerateDynamicColumns()
        {
            JobsGrid.Columns.Clear();

            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Srl", Binding = new System.Windows.Data.Binding("Srl"), Width = 80 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "SO No", Binding = new System.Windows.Data.Binding("So"), Width = 120 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Date", Binding = new System.Windows.Data.Binding("Date"), Width = 120 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Part No", Binding = new System.Windows.Data.Binding("Part_No"), Width = 150 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Nomen", Binding = new System.Windows.Data.Binding("Nomen"), Width = 200 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Qty", Binding = new System.Windows.Data.Binding("Qty"), Width = 80 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Vendor", Binding = new System.Windows.Data.Binding("Vend"), Width = 140 });
            JobsGrid.Columns.Add(new DataGridTextColumn { Header = "Status", Binding = new System.Windows.Data.Binding("Status"), Width = 120 });
        }

        // ---------------------------------------------------------
        // SEARCH FUNCTIONALITY
        // ---------------------------------------------------------
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_backupList == null) return;

            string key = SearchBox.Text.Trim().ToLower();
            string column = ColumnSelector.SelectedItem?.ToString();

            if (string.IsNullOrWhiteSpace(key))
            {
                ResetOrders();
                return;
            }

            var filtered = _backupList.Where(item =>
            {
                var prop = item.GetType().GetProperty(column)?.GetValue(item, null);
                if (prop == null) return false;
                return prop.ToString().ToLower().Contains(key);
            });

            Orders.Clear();
            foreach (var d in filtered)
                Orders.Add(d);
        }

        private void ResetOrders()
        {
            Orders.Clear();
            foreach (var d in _backupList)
                Orders.Add(d);
        }

        // ---------------------------------------------------------
        // FILTER BY LAST X DAYS
        // ---------------------------------------------------------
        private void DaysFilterBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (_backupList == null) return;

            string selected = (DaysFilterBox.SelectedItem as ComboBoxItem)?.Content.ToString();
            int days = selected switch
            {
                "Last 7 Days" => 7,
                "Last 15 Days" => 15,
                "Last 30 Days" => 30,
                "Last 90 Days" => 90,
                _ => 0
            };

            if (days == 0)
            {
                ResetOrders();
                return;
            }

            DateTime cutoff = DateTime.Now.AddDays(-days);

            var filtered = _backupList.Where(d =>
            {
                if (DateTime.TryParse(d.Date?.ToString(), out DateTime dt))
                    return dt >= cutoff;
                return false;
            });

            Orders.Clear();
            foreach (var f in filtered)
                Orders.Add(f);
        }

        // ---------------------------------------------------------
        // LEFT PANEL BUTTONS
        // ---------------------------------------------------------
        private void SO_All_Click(object sender, RoutedEventArgs e)
        {
            ResetOrders();
        }

        private void SO_No_Click(object sender, RoutedEventArgs e)
        {
            var filtered = _backupList.Where(d => string.IsNullOrWhiteSpace(d.So));

            Orders.Clear();
            foreach (var d in filtered)
                Orders.Add(d);
        }

        // ---------------------------------------------------------
        // BACK BUTTON
        // ---------------------------------------------------------
        private void LogoButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }

        // ---------------------------------------------------------
        // FOOTER BUTTONS (placeholders)
        // ---------------------------------------------------------
        private void Print_DOS_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("DOS print not implemented.");
        }

        private void Print_Win_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Windows print not implemented.");
        }

        private void Print_Word_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Word export not implemented.");
        }

        private void Print_Preview_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Print preview not implemented.");
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
